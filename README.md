# Pixelation Baking
An add-on for Blender that pixelates, bakes and saves the base color textures of selected objects

## Features
* Easily pixelated textures
* Allows for multiple objects to be queued together and baked
* Easily adjustable settings

## Installation
1. Press the `Code` drop-down button
2. Press `Download ZIP` and store wherever you want
3. Open Blender and press `Edit (in the top left) -> Preferences -> Add-ons -> Install`
4. Find the `ZIP` file and double click it
5. Click on the checkbox next to the add-on

## Usage
Before baking, check your render settings. You will not have to worry about most render settings, as they will be set and reset automatically when using the add-on, but you must manually decide to use either the CPU or GPU. I have found the best results with the CPU, but it depends somewhat from computer to computer and how many objects are being processed at once. To switch between the two, you first have to switch your `Render Engine` from `Eevee` to `Cycles`, then you can switch between CPU and GPU Compute.

To use the add-on, simply press 'N' and you can access the add-on settings under the `Tool` sub-menu. After adjusting the settings, select all objects you want to pixelate and press `Pixelate and Bake`. This will result in each object getting a new texture created and saved at your specified save location.

## IMPORTANT:
Make sure all objects have unique names, or certain textures will be overwritten!

## License
This package is licensed under the MIT License. For more information read: `LICENSE`.
