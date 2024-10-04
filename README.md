# Van Gogh Style Transfer with ComfyUI


![ComfyUI_00287_](https://github.com/user-attachments/assets/1236bfa1-05c2-4f47-b7fa-0d6345f068aa)
![ComfyUI_00289_](https://github.com/user-attachments/assets/622415fe-1a3c-4c9e-9220-70bc9a941fcc)


## Introduction

This project demonstrates how to use **ComfyUI**, **Stable Diffusion**, and **ControlNet** to perform style transfer, converting a user-provided image into a Van Gogh-style artwork. The workflow leverages the strengths of deep learning and image processing techniques to achieve a visually appealing result that mimics Van Gogh's artistic style.

The case study focuses on setting up an efficient workflow using ComfyUI and integrating advanced models like Stable Diffusion for the style transfer. This document will guide you through the setup process, usage, and troubleshooting, making it easy for anyone to replicate the results.

## Requirements
- **Python**: Required for running the API script and managing the backend processes.
- **ComfyUI**: The user interface for managing workflows and integrating different components of the style transfer process.
- **Stable Diffusion**: A deep learning model for generating images in various styles, including Van Gogh.
- **ControlNet**: A neural network that enhances the style transfer process by providing more precise control over the output.

## Setup

### Step 1: Installing ComfyUI

1. Clone the ComfyUI repository to your local machine:
    ```bash
    git clone https://github.com/comfyanonymous/ComfyUI.git
    ```
2. Navigate to the ComfyUI directory:
    ```bash
    cd ComfyUI
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Step 2: GPU Setup

#### NVIDIA GPUs:

To install stable PyTorch for NVIDIA:
```bash
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu124
```

For the nightly version with potential performance improvements:
```bash
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124
```

#### AMD GPUs (Linux Only):

To install the stable version of PyTorch for AMD GPUs:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.1
```

For the nightly version with potential performance enhancements (ROCm 6.2):
```bash
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.2
```

#### DirectML (AMD on Windows):
For AMD GPUs on Windows, use the DirectML backend:
```bash
pip install torch-directml
```

To launch ComfyUI with DirectML support, use:
```bash
python main.py --directml
```

#### Intel GPUs:
1. Install the necessary drivers and kernels from Intel's Extension for Pytorch (IPEX) [Installation page](https://www.intel.com).
2. Follow the instructions for installing Intel's **oneAPI Basekit**.
3. After installing IPEX, continue with the ComfyUI installation instructions.

#### Apple Mac (M1/M2):
1. Install the nightly build of PyTorch following the instructions in the [Apple Developer Guide](https://developer.apple.com/metal/pytorch).
2. Proceed with the ComfyUI installation instructions for Windows/Linux.

### Step 3: Adding Models


1. Download the following models:
    - **Stable Diffusion Checkpoint**: `realDreamVanGogh_1.safetensors`
    - https://civitai.com/models/146723/real-dream-van-gogh-edition
    - **ControlNet Model**: `controlnetMyseeEdgeDrawing_02.safetensors`
    - https://civitai.com/models/149740/controlnet-mysee-edge-drawing-parameter-free-easy-and-hassle-free-canny-alternative
2. Place the **Stable Diffusion checkpoint** in the following directory:
    ```
    models/checkpoints
    ```
3. Place the **ControlNet model** in:
    ```
    models/controlnet
    ```
4. Optionally, if you need to download a VAE model, place it in:
    ```
    models/vae
    ```


---

### Step 4: Installing ComfyUI Manager and Custom Nodes

To further enhance the functionality of ComfyUI, you can install the **ComfyUI Manager** and additional custom nodes. Follow the steps below to install the manager and add the necessary custom nodes for your project.

#### 1. Installing ComfyUI Manager

The ComfyUI Manager is a tool to simplify the management of custom nodes. To install it on top of your existing ComfyUI installation, follow these steps:

1. Open your terminal (or command prompt) and navigate to the `custom_nodes` directory of your ComfyUI installation:
    ```bash
    cd ComfyUI/custom_nodes
    ```
2. Clone the ComfyUI Manager repository:
    ```bash
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git
    ```
3. After cloning, restart ComfyUI:
    ```bash
    python main.py
    ```

#### 2. Adding Custom Nodes via ComfyUI Manager

Once ComfyUI Manager is installed and ComfyUI is restarted, follow these steps to add custom nodes:

1. Open the **Custom Nodes Manager** from the ComfyUI Manager interface.
2. Click on **Install via Git URL**.
3. For each custom node, enter the following GitHub URLs one by one and install them:

   - **Art Venture**: 
     ```bash
     https://github.com/sipherxyz/comfyui-art-venture
     ```
   - **ControlNet Auxiliary**:
     ```bash
     https://github.com/Fannovel16/comfyui_controlnet_aux
     ```
   - **Comfyroll Custom Nodes**:
     ```bash
     https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes
     ```

4. After installing all the custom nodes, restart ComfyUI again to ensure that the nodes are properly integrated.

---

### Step 5: Loading and Configuring the Van Gogh Workflow

Once ComfyUI is running, follow these steps to load and configure the Van Gogh style transfer workflow:

#### 1. Load the Workflow

1. Launch ComfyUI using the command:
    ```bash
    python main.py
    ```
2. Once the interface is loaded, click on the **Load Workflow** button in the top-right corner.
3. Select the `van_gogh_workflow.json` file from your local system and load it into ComfyUI.

#### 2. Model Settings

In the **Model** section of the workflow, ensure that the following models are correctly configured:
- **Stable Diffusion Checkpoint**: `realDreamVanGogh_1.safetensors`
  - This file should be located in: `models/checkpoints/realDreamVanGogh_1.safetensors`
- **ControlNet Model**: `controlnetMyseeEdgeDrawing_02.safetensors`
  - This file should be located in: `models/controlnet/controlnetMyseeEdgeDrawing_02.safetensors`

#### 3. ControlNet Settings

In the **ControlNet** section, configure the following settings:
- **Preprocessor**: Set to `lineart`
- **Strength**: 0.56 (This controls how strongly the style is applied to the input image. Adjust if necessary.)

#### 4. Sampler Parameters

In the **Sampler Parameters** section, ensure the following settings are configured:
- **Steps**: 20-50 (This determines the number of diffusion steps. Start with 20 and adjust as needed.)
- **CFG Scale**: 7.1 (This influences how closely the generated image follows the prompt.)
- **Sampler**: `dpmpp_2m`
- **Resolution**: 768x788
- **Denoising Strength**: 0.52 (Lower values maintain more details from the original image.)

#### 5. Prompt

The current prompt is set to describe a Van Gogh-style painting. You can modify the prompt to change the artistic direction if needed. The default prompt is:
```text
A painting in the style of Vincent van Gogh, with vivid brushstrokes, bold colors, swirling patterns, heavy use of contrast, and dynamic composition.
```

#### 6. Image Input

To process an image:
1. Upload an image using the **Image** node in the workflow.
2. The processed output will appear as a Van Gogh-style version of the uploaded image.

### Final Step: Testing and Experimentation

After all the settings are configured, experiment with different images, prompts, and parameters to achieve the desired results.


---

# Additional: Running the API Script for Automated Workflow

This section explains how to run an API script to automate the entire Van Gogh-style image processing workflow without using the ComfyUI interface.

#### Prerequisites

Before running the script, ensure the following:
1. **ComfyUI's `main.py` must be running** and connected to the local server at `127.0.0.1:8188`.

2. The necessary files must be prepared:
   - Input Image: The image you want to process.
   - Stable Diffusion Checkpoint: The model file.
   - ControlNet Model: The ControlNet file.
   - Workflow JSON: The workflow definition file.

#### Steps to Run the API Script

1. **Start ComfyUI**:
   
   Make sure ComfyUI is running before executing the script. Use the following command to start ComfyUI:
   ```bash
   python main.py
   ```

2. **Prepare the Files**:
   
   Ensure that the following files are ready:
   - Input image (e.g., `input_image.png`)
   - Stable Diffusion checkpoint (e.g., `realDreamVanGogh_1.safetensors`)
   - ControlNet model (e.g., `controlnetMyseeEdgeDrawing_02.safetensors`)
   - Workflow JSON (e.g., `van_gogh_workflow_api.json`)


3. **Run the Script**:
   
   After starting the ComfyUI server, run the API script with the necessary arguments as follows:
   
   ```bash
   python van_gogh_script.py --image_path "path/to/input_image.png" --checkpoint_path "path/to/realDreamVanGogh_1.safetensors" --controlnet_path "path/to/controlnetMyseeEdgeDrawing_02.safetensors" --json_path "path/to/van_gogh_workflow_api.json"
   ```

   - Replace `"path/to/input_image.png"` with the path to your input image.
   - Replace `"path/to/realDreamVanGogh_1.safetensors"` with the path to the Stable Diffusion checkpoint file.
   - Replace `"path/to/controlnetMyseeEdgeDrawing_02.safetensors"` with the ControlNet model file.
   - Replace `"path/to/van_gogh_workflow_api.json"` with the path to your workflow JSON file.

#### Outputs

- Once the script finishes execution, a Van Gogh-style image will be generated based on the parameters defined in the workflow and saved to the appropriate location.
- The script interacts with the local ComfyUI server via WebSocket, so make sure that the server is up and running.

#### Notes

- Ensure that the ComfyUI server is running on `127.0.0.1:8188`, or modify the server address in the script if using a different IP or port.
- Double-check that all paths provided to the script are correct and accessible.
- This script allows you to automate the entire workflow without needing to interact with the ComfyUI interface manually.
