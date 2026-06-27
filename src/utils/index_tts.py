"""IndexTTS2 文本转语音工具。"""

from __future__ import annotations

import argparse
import os
import threading
import uuid
from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "src" / "resource" / "audio"
DEFAULT_VOICE_PATH = (
    PROJECT_ROOT / "src" / "resource" / "indextts" / "sample_prompt.wav"
)

_INFERENCE_LOCK = threading.Lock()


def _required_path(env_name: str, default: Path | None = None) -> Path:
    raw_value = os.getenv(env_name)
    path = Path(raw_value).expanduser() if raw_value else default
    if path is None:
        raise RuntimeError(f"请配置环境变量 {env_name}")

    if not path.is_absolute():
        path = PROJECT_ROOT / path
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(f"{env_name} 指向的路径不存在：{path}")
    return path


@lru_cache(maxsize=1)
def _get_tts() -> Any:
    """延迟加载并复用模型，避免每次合成都重新载入权重。"""
    try:
        from indextts.infer_v2 import IndexTTS2
    except ModuleNotFoundError as exc:
        missing_package = exc.name or "未知依赖"
        raise RuntimeError(
            f"当前 Python 环境缺少 IndexTTS2 运行依赖：{missing_package}。"
            "请使用 IndexTTS 官方虚拟环境运行，或按照官方文档安装完整依赖；"
            "不要只安装单个缺失包。"
        ) from exc

    model_dir = _required_path(
        "INDEXTTS_MODEL_DIR", PROJECT_ROOT / "checkpoints"
    )
    config_path = model_dir / "config.yaml"
    if not config_path.is_file():
        raise FileNotFoundError(f"IndexTTS 配置文件不存在：{config_path}")

    # IndexTTS2 源码会把 HF_HUB_CACHE 设置成相对路径
    # ./checkpoints/hf_cache。这里改为模型目录下的绝对路径，避免缓存位置
    # 随 PyCharm Working directory 改变。
    os.environ["HF_HUB_CACHE"] = str(model_dir / "hf_cache")

    return IndexTTS2(
        cfg_path=str(config_path),
        model_dir=str(model_dir),
        use_fp16=os.getenv("INDEXTTS_USE_FP16", "false").lower() == "true",
        use_cuda_kernel=(
            os.getenv("INDEXTTS_USE_CUDA_KERNEL", "false").lower() == "true"
        ),
        use_deepspeed=(
            os.getenv("INDEXTTS_USE_DEEPSPEED", "false").lower() == "true"
        ),
    )


def generate_speech(text: str) -> tuple[str, str]:
    """将文本合成为本地 WAV 音频并返回绝对路径和项目相对路径。

    Args:
        text: 要合成的非空文本。

    Returns:
        ``(absolute_path, relative_path)``，两个值均为字符串。

    配置：
        - ``INDEXTTS_MODEL_DIR``：模型目录，默认 ``<项目根>/checkpoints``。
        - 模型配置固定读取 ``<模型目录>/config.yaml``。
        - 参考音频默认读取 ``src/resource/indextts/sample_prompt.wav``。
        - ``INDEXTTS_OUTPUT_DIR``：输出目录，默认 ``src/resource/audio``。
    """
    normalized_text = text.strip()
    if not normalized_text:
        raise ValueError("text 不能为空")

    voice_path = _required_path("INDEXTTS_VOICE", DEFAULT_VOICE_PATH)
    configured_output_dir = os.getenv("INDEXTTS_OUTPUT_DIR")
    output_dir = (
        Path(configured_output_dir).expanduser()
        if configured_output_dir
        else DEFAULT_OUTPUT_DIR
    )
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir
    output_dir = output_dir.resolve()
    try:
        output_dir.relative_to(PROJECT_ROOT)
    except ValueError as exc:
        raise ValueError(
            "INDEXTTS_OUTPUT_DIR 必须位于项目根目录内，才能返回项目相对路径"
        ) from exc
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{uuid.uuid4().hex}.wav"
    with _INFERENCE_LOCK:
        _get_tts().infer(
            spk_audio_prompt=str(voice_path),
            text=normalized_text,
            output_path=str(output_path),
            verbose=False,
        )

    if not output_path.is_file():
        raise RuntimeError(f"IndexTTS 未生成预期的音频文件：{output_path}")

    absolute_path = output_path.resolve()
    relative_path = absolute_path.relative_to(PROJECT_ROOT)

    return str(absolute_path), relative_path.as_posix()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="测试 IndexTTS2 文本转语音")
    parser.add_argument(
        "text",
        nargs="?",
        default="你好，这是 IndexTTS 语音合成测试。",
        help="需要合成的文本",
    )
    args = parser.parse_args()

    audio_absolute_path, audio_relative_path = generate_speech(args.text)
    print(f"音频绝对路径：{audio_absolute_path}")
    print(f"项目相对路径：{audio_relative_path}")
