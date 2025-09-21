# RVC Text-to-Speech WebUI

This is a text-to-speech Gradio webui for [RVC](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) models, using [edge-tts](https://github.com/rany2/edge-tts).

[🤗 Online Demo](https://huggingface.co/spaces/litagin/rvc_okiba_TTS)

This can run on CPU without GPU (but slow).

![Screenshot](assets/screenshot.jpg)

## Install

Requirements: Tested for Python 3.10 on Windows 11. Python 3.11 is probably not supported, so please use Python 3.10.

```bash
git clone https://github.com/litagin02/rvc-tts-webui.git
cd rvc-tts-webui

# Download models in root directory
curl -L -O https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/hubert_base.pt
curl -L -O https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt

# Make virtual environment
python -m venv venv
# Activate venv (for Windows)
venv\Scripts\activate

# Install PyTorch manually if you want to use NVIDIA GPU (Windows)
# See https://pytorch.org/get-started/locally/ for more details
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install requirements
pip install -r requirements.txt
```

## Locate RVC models

Place your RVC models in `weights/` directory as follows:

```bash
weights
├── model1
│   ├── my_model1.pth
│   └── my_index_file_for_model1.index
└── model2
    ├── my_model2.pth
    └── my_index_file_for_model2.index
...
```

Each model directory should contain exactly one `.pth` file and at most one `.index` file. Directory names are used as model names.

It seems that non-ASCII characters in path names gave faiss errors (like `weights/モデル1/index.index`), so please avoid them.

## Launch

```bash
# Activate venv (for Windows)
venv\Scripts\activate

python app.py
```

## Update

```bash
git pull
venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

## Troubleshooting

```
error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for fairseq
Failed to build fairseq
ERROR: Could not build wheels for fairseq, which is required to install pyproject.toml-based projects
```

Maybe fairseq needs Microsoft C++ Build Tools.
[Download installer](https://visualstudio.microsoft.com/ja/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16) and install it.

```
(1) In PyTorch 2.6, we changed the default value of the `weights_only` argument in `torch.load` from `False` to `True`. Re-running `torch.load` with `weights_only` set to `False` will likely succeed, but it can result in arbitrary code execution. Do it only if you got the file from a trusted source.
(2) Alternatively, to load with `weights_only=True` please check the recommended steps in the following error message.
WeightsUnpickler error: Unsupported global: GLOBAL fairseq.data.dictionary.Dictionary was not an allowed global by default. Please use `torch.serialization.add_safe_globals([fairseq.data.dictionary.Dictionary])` or the `torch.serialization.safe_globals([fairseq.data.dictionary.Dictionary])` context manager to allowlist this global if you trust this class/function.
```

Maybe you need to fix `venv\Lib\site-packages\fairseq\checkpoint_utils.py` line 315 to read weights.

```
state = torch.load(f, map_location=torch.device("cpu"), weights_only=False)
```