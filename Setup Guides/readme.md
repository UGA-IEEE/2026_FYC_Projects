## Visual Studio Code Install

Visual Studio Code (VS Code) is a code editor with integrated development environment (IDE) capabilities similar to Visual Studio, Eclipse, or IntelliJ. Visual Studio differs from VS Code in that it is a complete IDE. 

VS Code does not include any integrated compilers, which means C compilers must be installed separately. With additional compilers and extensions, VS Code can be configured to function as a lightweight IDE.


**VS Code Download (Windows, Linux, Mac):** https://code.visualstudio.com/download

<br>

## Git Install & Git Clone

Git is a distributed version control system (DVCS) that utilizes command-line operations. A version control system enables engineers and developers to view the version history, track changes, facilitate branching, and promote collaboration. 

Since Git is a DVCS, it has more advantages compared to a standard VCS. The most prominent difference is that Git allows every developer to have a full copy of the entire repository, including its version history by using git clone

<details>
<summary><strong>Steps:</strong></summary>

1. <u>Open VS Code and click on the profile button in the bottom left corner. Press sign in with GitHub. You will need to make a GitHub account if you do not have one. (Personal Email). </u>

    <details>

    <summary>Click to expand</summary> 

    | Before | After |
    |-------|-------|
    | <img src="image-1.png" width="300"> | <img src="image-2.png" width="300"> |

    </details>
<br>

2. <u>Open a new terminal if one is not already shown.</u>

    <details>
    <summary>Click to expand</summary>
    <img src="Images\image-3.png"  width="500"> 
    </details>



<br>

3. <u>Check to see if Git is already installed by typing `git status` in the terminal. If it is not installed OR does not have an environmental path, the following error will appear:</u>

    <details>
    <summary>Click to expand</summary>
    <img src="Images\image-5.png"  width="900"> 
    </details>

    <br>

    If the error message does not appear and Git is installed, proceed to **STEP 7**

<br>

4. <u>Download Git if not installed. Use all default settings during the selection.</u>

    **Git Download(Windows, Linux, Mac):**  https://git-scm.com/downloads

<br>

5. <u>**(Windows)** Ensure your system variables is updated. Otherwise, the following message may appear:</u>

    `'git' is not recognized as an internal or external command`

    <details>
    <summary>Click to expand</summary>
    a. In the Windows search bar, type edit system environmental variables

    <img src="Images\image-7.png" width="300"> 

    b. Select Environment Variables

    <img src="Images\image-8.png"  width="400"> 

    c. Under System Variables, select Path, and press edit

    <img src="Images\image-11.png" width="400"> 

    d. Create a New Variable and type `C:\Program Files\Git\cmd` or wherever the cmd is stored.

    <img src="Images\image-12.png" width="400">
    </details>

<br>

6. <u>Type `git' in the terminal, and the following output should appear.</u>

    <details>
    <summary>Click to expand</summary>  
    <img src="Images\image-6.png"  width="600"> 
    </details>
    
<br>

7. <u>Clone the GitHub Repo (HTTPS) from the terminal in VS Code. If permission is denied, ensure that you have been added to the organization and the account you are using is the one associated with the organization on GitHub.</u>

    ```bash
    git clone https://github.com/UGA-IEEE/2026_FYC_Projects.git
    ```
    <details>
    <summary>Click to expand</summary>  
    <img src="Images\image-14.png" width="600"> 
    </details>

    <br>

    **(Windows)** If you are unable to clone the repo due to the account not having permission, double-check in the credential manager that the account associated with the UGA IEEE organization is listed. If not, then edit the credential. 
        <details>
        <summary>Click to expand</summary>  
        <img src="Images\image-13.png"  width="400"> 
        </details>

<br>

8. <u>Ensure the repo appears as a folder in your directory by typing </u> `ls`.<u>You can always relocate the repository's location if desired, since it is a folder.</u>

    <details>
    <summary>Click to expand</summary>  
    <img src="Images\image-15.png"  width="400">
    </details>

<br>

9. <u>Open the folder and select the repo.</u>

    <details>
    <summary>Click to expand:</summary>
    <img src="Images\image-18.png"  width="400">
    </details>

<br>

10. <u>Configure Git username and email by using your actual name, e.g, Jane Doe, and the email associated with your GitHub account.</u>

    ```bash
    git config --global user.name  "Your Full Name"
    git config --global user.email "your_email@example.com"
    ```

    <details>
    <summary>The following message will appear if GitHub not configured in VS Code:</summary>
    <img src="Images\image-19.png"  width="400">
    </details>


<br>
</details>

## C Compiler Install (Windows)



Since VS Code is just an code editor, a C Compiler must be installed separately. The compiler will convert the C code into machine code and create an executable file that the device can run.

MSY32 (Minimal SYStem 2) is a software environment for Windows that can be utilized to install compilers. 

```C
// TEST CODE: hello_world.c

#include <stdio.h>   // Standard I/O - needed for printf

int main(void) {
    printf("Hello, World!\n");  
    return 0;                   // End program
}
```
<br>

<details>
<summary><strong>Steps:</strong></summary>

1. <u>Create a file named hello_world.c and ensure your current working directory has the file in it. Copy paste the code. Use </u> `cd` <u>to change directories</u>

    <details>
    <summary>Click to expand:</summary>
    <img src="Images\image-20.png"  width="10000">
    </details>


<br>

2. <u>Check if you have a C Compiler by typing</u> `gcc hello_world.c -o hello`

    <details>
    <summary>Click to expand:</summary>
    <img src="Images\image-21.png"  width="10000">
    </details>

    <br>

    If you are able to run the gcc command, proceed to **Step 5**


<br>

3. <u>Follow the steps (1-8) and download MSY2</u> https://www.msys2.org/ 

    <br>

    The following message will appear once you finish and type `which gcc`:
        <details>
        <summary>Click to expand:</summary>
        <img src="Images\image-22.png"  width="400">
        </details>

<br>

4. <u>Ensure your system variables is updated. Otherwise, the C compiler will not be recongized</u>


    <details>
    <summary>Click to expand</summary>
    a. In the Windows search bar, type edit system environmental variables

    <img src="Images\image-7.png" width="300"> 

    b. Select Environment Variables

    <img src="Images\image-8.png"  width="400"> 

    c. Under System Variables, select Path, and press edit

    <img src="Images\image-11.png" width="400"> 

    d. Create a New Variable and type `C:\msys64\ucrt64\bin` or wherever the files is stored.

    <img src="Images\image-24.png" width="400">
    </details>

<br>

5. Close VS Code and reopen it. Run the following commands in the terminal.:

    ```bash
    gcc hello_world.c -o hello
    ./hello
    ```

    | Command       | Purpose          
    | ------------- |:-------------| 
    | gcc           |Invokes the GNU Compiler Collection, which can compile C code.
    | hello_world.c |The source file written in C that needs to be compiled. GCC reads this file and converts it into machine code
    | -o            |Stands for output. Allows the name of the resulting executable to specified
    | hello         |The name of the executable that will be generated
    | ./hello       | Runs the compiled program

    <br>

    <details>
    <summary>Click to expand:</summary>
    <img src="Images\image-25.png"  width="800">
    </details>

</details>