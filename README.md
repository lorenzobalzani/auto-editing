<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![Open issues][open-issues-shield]][open-issues-url]
[![Closed issues][closed-issues-shield]][closed-issues-url]
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/lorenzobalzani/auto-editing?style=for-the-badge)
[![Forks][forks-shield]][forks-url]
[![Apache License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <!-- <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h3 align="center">Auto editing software</h3>

  <p align="center">
    Auto edit (e.g. cut) video files by leveraging gesture recognition.
    <br />
    <a href="https://github.com/lorenzobalzani/auto-editing/fork">Fork</a>
    ·
    <a href="https://github.com/lorenzobalzani/auto-editing/issues">Report Bug</a>
    ·
    <a href="https://github.com/lorenzobalzani/auto-editing/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#launch">Launch</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
TODO
<!--There are many great README templates available on GitHub, however, I didn't find one that really suit my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need -- I think this is it.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should implement DRY principles to the rest of your life :smile:

Of course, no one template will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. Thanks to all the people have contributed to expanding this template!

A list of commonly used resources that I find helpful are listed in the acknowledgements. -->

### Built With
* [Python 3.8](https://www.python.org)
* [MoviePy](https://github.com/Zulko/moviepy)
* [Tensorflow 2](https://github.com/tensorflow/tensorflow)
* [OpenCV](https://github.com/opencv/opencv)

### Prerequisites
Before launching any Python file in the repo, be sure to install the required dependencies by typing in your terminal:
  ```sh
  pip install -r requirements.txt
  ```
  
### Launch
To launch the application from the *CLI*, navigate to the application's root directory and type the following commands:
```sh
  python3 app.py
```
A brief guide will pop up:
```sh
  python3 app.py [-h] -v VIDEO [-i INTRO] [-o OUTPUT] [-c COMPRESSION] [-q QUALITY] [-vc VCODEC] [-t THREADS] [-d DEBUG]
```
As you can see, only the argument `video` is mandatory, while the others have default values. For a more comprehensive list of arguments, type the following commands:
```sh
  python3 app.py -h
```
The complete helper will be displayed:

```console
usage: app.py [-h] -v VIDEO [-i INTRO] [-o OUTPUT] [-c COMPRESSION] [-q QUALITY] [-vc VCODEC] [-t THREADS] [-d DEBUG]

Help for auto editing software.

optional arguments:
  -h, --help            show this help message and exit
  -v VIDEO, --video VIDEO
                        Path to the original video. (default: None)
  -i INTRO, --intro INTRO
                        Path to the intro. (default: None)
  -o OUTPUT, --output OUTPUT
                        Path to the output video. (default: output)
  -c COMPRESSION, --compression COMPRESSION
                        Compression value. Possible values: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow. (default:
                        medium)
  -q QUALITY, --quality QUALITY
                        Video quality. 51: the worst - 0: the best (lossless). (default: 10)
  -vc VCODEC, --vcodec VCODEC
                        Video codec. (default: libx264)
  -t THREADS, --threads THREADS
                        Number of threads. (default: 1)
  -d DEBUG, --debug DEBUG
                        Export the whole video w/ printed gestures and classifications. (default: False)
```

## Usage

The following list includes currently supported gestures:
 * insert video intro: opened hand sign (N_GESTURE = 1);
 * cut between timestamps: closed hand sign (N_GESTURE = 2).

:warning: **Be sure to horizontally flip your video before using the software.** :warning:

<!-- ROADMAP -->
## Roadmap
See the [open issues](https://github.com/lorenzobalzani/auto-editing/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. To contribute, please refer to the following procedure:

1. Open an issue, tag it with the most relevant label and write a couple of rows about what task you'd like to perform.
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature #ISSUE_NUMBER'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License
Distributed under the Apache License 2.0. See [`LICENSE.txt`](https://github.com/lorenzobalzani/auto-editing/blob/master/LICENSE.txt) for more information.


<!-- CONTACT -->
## Contact
<a href="https://www.linkedin.com/in/lorenzobalzani/"><img src="https://www.vectorlogo.zone/logos/linkedin/linkedin-icon.svg" width="30px" alt="linkedin"></a>
&nbsp; &nbsp;
<a href="mailto:balzanilo@gmail.com"><img src="https://www.vectorlogo.zone/logos/gmail/gmail-icon.svg" width="30px" alt="mail"></a> 
&nbsp; &nbsp;
<a href="mailto:balzanilo@icloud.com"><img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Mail_%28iOS%29.svg" width="30px" alt="mail"></a> 
&nbsp; &nbsp;
<a href="mailto:lorenzo.balzani@studio.unibo.it"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Seal_of_the_University_of_Bologna.svg/1920px-Seal_of_the_University_of_Bologna.svg.png" width="30px" alt="mail"></a> 
&nbsp; &nbsp;
<a href="https://lorenzobalzani.github.io/"><img src="https://images.vexels.com/media/users/3/205387/isolated/preview/9e5a4a16e78a187fc3e47fc6e2c5f03a-internet-website-icon-stroke.png" width="30px" alt="website"></a> 
</br>
If you have any questions/feedback, please do not hesitate to reach out to me! 💬

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/lorenzobalzani/auto-editing.svg?style=for-the-badge
[contributors-url]: https://github.com/lorenzobalzani/auto-editing/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/lorenzobalzani/auto-editing.svg?style=for-the-badge
[forks-url]: https://github.com/lorenzobalzani/auto-editing/network/members
[stars-shield]: https://img.shields.io/github/stars/lorenzobalzani/auto-editing.svg?style=for-the-badge
[stars-url]: https://github.com/lorenzobalzani/auto-editing/stargazers
[open-issues-shield]: https://img.shields.io/github/issues/lorenzobalzani/auto-editing.svg?style=for-the-badge
[open-issues-url]: https://github.com/lorenzobalzani/auto-editing/issues
[closed-issues-shield]: https://img.shields.io/github/issues-closed/lorenzobalzani/auto-editing.svg?style=for-the-badge
[closed-issues-url]: https://github.com/lorenzobalzani/auto-editing/issues-closed
[license-shield]: https://img.shields.io/github/license/lorenzobalzani/auto-editing.svg?style=for-the-badge
[license-url]: https://github.com/lorenzobalzani/auto-editing/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/lorenzobalzani
[product-screenshot]: images/screenshot.png
