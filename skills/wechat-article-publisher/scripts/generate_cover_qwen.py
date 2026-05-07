#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
"""
Generate images using Qwen Image API (Alibaba Cloud DashScope).

Usage:
    uv run generate_image.py --prompt "your image description" --filename "output.png" [--model qwen-image-max|qwen-image-turbo] [--size 1664*928|1024*1024|720*1280|1280*720] [--api-key KEY]
"""

import argparse
import os
import sys
import json
import base64
from pathlib import Path


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("DASHSCOPE_API_KEY")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Qwen Image API"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description/prompt"
    )
    parser.add_argument(
        "--filename", "-f",
        help="Output filename (optional, if not provided will only return URL)"
    )
    parser.add_argument(
        "--model", "-m",
        choices=["qwen-image-max", "qwen-image-turbo", "qwen-image-plus-2026-01-09"],
        default="qwen-image-max",
        help="Model to use: qwen-image-max (default) or qwen-image-turbo"
    )
    parser.add_argument(
        "--size", "-s",
        choices=["1664*928", "1024*1024", "720*1280", "1280*720"],
        default="1664*928",
        help="Output size (default: 1664*928 for 16:9 ratio)"
    )
    parser.add_argument(
        "--negative-prompt", "-n",
        default="低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。",
        help="Negative prompt to avoid unwanted elements"
    )
    parser.add_argument(
        "--no-prompt-extend",
        action="store_true",
        help="Disable automatic prompt enhancement"
    )
    parser.add_argument(
        "--watermark",
        action="store_true",
        help="Add watermark to generated image"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="DashScope API key (overrides DASHSCOPE_API_KEY env var)"
    )
    parser.add_argument(
        "--no-verify-ssl",
        action="store_true",
        help="Disable SSL certificate verification (use with caution)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set DASHSCOPE_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # Import here after checking API key
    import requests

    # Set up output path

    # Build request payload
    payload = {
        "model": args.model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": args.prompt
                        }
                    ]
                }
            ]
        },
        "parameters": {
            "negative_prompt": args.negative_prompt,
            "prompt_extend": not args.no_prompt_extend,
            "watermark": args.watermark,
            "size": args.size
        }
    }

    print(f"Generating image with {args.model}...")
    print(f"Size: {args.size}")
    print(f"Prompt: {args.prompt}")

    try:
        # Make API request
        response = requests.post(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json=payload,
            timeout=120,
            verify=True
        )

        response.raise_for_status()
        result = response.json()

        # Check for errors
        if result.get("code"):
            error_msg = result.get("message", "Unknown error")
            print(f"API Error: {error_msg}", file=sys.stderr)
            sys.exit(1)

        # Extract image URL from response
        output_data = result.get("output", {})
        choices = output_data.get("choices", [])
        
        if not choices:
            print("Error: No choices in response", file=sys.stderr)
            print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
            sys.exit(1)

        # Get image URL from first choice
        message = choices[0].get("message", {})
        content = message.get("content", [])
        
        if not content or not content[0].get("image"):
            print("Error: No image URL in response", file=sys.stderr)
            print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
            sys.exit(1)

        image_url = content[0]["image"]
        print(f"\nImage URL: {image_url}")

        # If filename is provided, download and save the image
        if args.filename:
            output_path = Path(args.filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            print("Downloading image...")
            img_response = requests.get(image_url, timeout=30, verify=not args.no_verify_ssl)
            img_response.raise_for_status()

            # Save the image
            with open(output_path, "wb") as f:
                f.write(img_response.content)

            full_path = output_path.resolve()
            print(f"Image saved: {full_path}")
            # Clawdbot parses MEDIA tokens and will attach the file on supported providers.
            print(f"MEDIA: {full_path}")
        else:
            # Just return the URL for Clawdbot to display
            print(f"MEDIA_URL: {image_url}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}", file=sys.stderr)
        try:
            error_detail = response.json()
            print(f"Error details: {json.dumps(error_detail, indent=2, ensure_ascii=False)}", file=sys.stderr)
        except:
            print(f"Response text: {response.text}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
