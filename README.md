```
```
#
``` LambScan
```
# LambScan
Robolab's LambScan project.

This project uses the [Intel's RealSense Library](https://github.com/IntelRealSense/librealsense) for
 their [D400 series cameras](https://www.intelrealsense.com/depth-camera-d415/).

At the moment of this development, the RealSense SDK only supports Ubuntu LTS kernels 4.4, 4.8, 4.10, 4.13, 4.15 and 4.18.
So, you should downgrade the kernel to use this code in order to use the DKMS installer for Realsense SDK. Also, you can
build the library from the source and apply some manual patches to be able to run it.

## Configuration parameters
As any other component,
``` *LambScan* ```
needs a configuration file to start. In

    etc/config

you can find an example of a configuration file. We can find there the following lines:

    EXAMPLE HERE

    
## Starting the component
To avoid changing the *config* file in the repository, we can copy it to the component's home directory, so changes will remain untouched by future git pulls:

    cd

``` <LambScan 's path> ```

    cp etc/config config
    
After editing the new config file we can run the component:

    bin/

```LambScan ```

    --Ice.Config=config
