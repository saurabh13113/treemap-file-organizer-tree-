# treemap-file-organizer 🌲
# University project that makes use of file system trees and treemaps to organize files and folders using a visual system.

As a software developer, I created an interactive treemap visualization tool to display hierarchical data structures, specifically focusing on file system trees. A treemap uses rectangles to represent files and folders, with the size of each rectangle proportional to the size of the data it represents. This allows for a clear visual representation of how storage is distributed across a file system.

The visual representation is as shown below:
![image](https://github.com/saurabh13113/treemap-file-organizer-tree-/assets/107759922/ab8ab100-f833-4c00-b4a6-fa5e7d4d9161)


In developing this tool, I utilized Object-Oriented Programming (OOP) principles to create a general API. The base class models the hierarchical nature of the data, with nodes representing files and folders. I then defined a specific subclass to handle the visualization of a computer's file system. Each file and folder is represented as a node with an associated size, reflecting either the file's size or the cumulative size of files within a folder.

![image](https://github.com/saurabh13113/treemap-file-organizer-tree-/assets/107759922/1fc67c2d-306a-4ebb-8cf9-19c9970ca5a5)

The tool provides an interactive interface where users can explore their file system visually. By scaling rectangles based on file sizes, users can easily identify which files or folders occupy the most space. This approach is similar to popular disk usage visualization programs like WinDirStat for Windows, Disk Inventory X for OSX, and KDirStat for Linux. This visualization not only aids in understanding storage usage but also helps in identifying large or unnecessary files, making it a valuable tool for efficient file system management.

![image](https://github.com/saurabh13113/treemap-file-organizer-tree-/assets/107759922/02ff6507-0630-41cd-a509-f0bdb5fbbb2e)
![image](https://github.com/saurabh13113/treemap-file-organizer-tree-/assets/107759922/217c53f0-9ba6-4330-ba4c-1392513be198)
