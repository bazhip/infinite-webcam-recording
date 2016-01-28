This project works by taking snapshots from the webcam at 15 frames per second. It keeps around a buffer of the last 24 hours of pictures.

In the event that you want to save the snapshots, simply press the letter 'S' on your keyboard, and all the rolling buffer will be converted to a video.

If nothing important happens, the previous days snapshots will be overwritten. This way you don't fill up your harddrive.

This project is based off of [technobabbler's tutorial](http://technobabbler.com/?p=22) and requires Python 2.5, [VideoCapture](http://videocapture.sourceforge.net/), [PIL](http://www.pythonware.com/products/pil/), and [pygame](http://www.pygame.org/) to run.