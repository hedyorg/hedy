var $builtinmodule = function (name) {
    mod = {};
    mod.load = new Sk.builtin.func(function (filename) {
        function imageExists(imageUrl) {
            var http = new XMLHttpRequest();
            http.open('HEAD', imageUrl, false);
            http.send();
            return http.status === 200;
        }

        if (imageExists(Sk.imgPath + Sk.ffi.remapToJs(filename))) {
            return Sk.misceval.promiseToSuspension(new Promise(function (resolve) {
                var img = new Image();
                img.crossOrigin='';
                img.src = Sk.imgPath + Sk.ffi.remapToJs(filename);
                img.onload = function () {
                    var t = Sk.builtin.tuple([img.width, img.height]);
                    var s = Sk.misceval.callsim(PygameLib.SurfaceType, t);
                    var ctx = s.offscreen_canvas.getContext("2d");
                    ctx.drawImage(img, 0, 0);
                    resolve(s);
                };
            }));
        }
        else
            throw new Sk.builtin.RuntimeError("Image does not exist.");
    });
    mod.get_extended = new Sk.builtin.func(function () {
        return Sk.ffi.remapToPy(false);
    });
    mod.save = new Sk.builtin.func(function (surf, filename) {
        var fname = 'surface';
        if (filename !== undefined) {
            fname = Sk.ffi.remapToJs(filename);
        }
        // https://stackoverflow.com/a/34707543
        saveAsPNG(surf.offscreen_canvas, fname);

        function saveAsPNG(image, filename) { // No IE <11 support. Chrome URL bug for large images may crash
            var anchorElement, event, blob;

            function image2Canvas(image) {  // converts an image to canvas
                function createCanvas(width, height) {  // creates a canvas of width height
                    var can = document.createElement("canvas");
                    can.width = width;
                    can.height = height;
                    return can;
                }

                var newImage = canvas(img.width, img.height); // create new image
                newImage.ctx = newImage.getContext("2d");  // get image context
                newImage.ctx.drawImage(image, 0, 0); // draw the image onto the canvas
                return newImage;  // return the new image
            }

            if (image.toDataURL === undefined) {    // does the image have the toDataURL function
                image = image2Canvas(image);  // No then convert to canvas
            }
            // if msToBlob and msSaveBlob then use them to save. IE >= 10
            // As suggested by Kaiido
            if (image.msToBlob !== undefined && navigator.msSaveBlob !== undefined) {
                blob = image.msToBlob();
                navigator.msSaveBlob(blob, filename + ".png");
                return;
            }
            anchorElement = document.createElement('a');  // Create a download link
            anchorElement.href = image.toDataURL();   // attach the image data URL
            // check for download attribute
            if (anchorElement.download !== undefined) {
                anchorElement.download = filename + ".png";  // set the download filename
                if (typeof MouseEvent === "function") {   // does the browser support the object MouseEvent
                    event = new MouseEvent(   // yes create a new mouse click event
                        "click", {
                            view: window,
                            bubbles: true,
                            cancelable: true,
                            ctrlKey: false,
                            altKey: false,
                            shiftKey: false,
                            metaKey: false,
                            button: 0,
                            buttons: 1,
                        }
                    );
                    anchorElement.dispatchEvent(event); // simulate a click on the download link.
                } else if (anchorElement.fireEvent) {    // if no MouseEvent object try fireEvent
                    anchorElement.fireEvent("onclick");
                }
            }
        }
    });
    return mod;
};
