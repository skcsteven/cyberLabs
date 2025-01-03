## Flag Command 

#### 1: Initial Recon

The web app seems to be a simple story game where the user inputs certain commands and tries to "beat" the game.

There doesn't seem to be many attack surfaces or vulnerabilities besides the command entering for the game. Subdomain searches with Gobuster and dirb also yielded no hidden pages.

The best bet in this case is to check the underlying html, css, js using the browser dev tools.

#### 2. Inspecting page with Developer Tools

There doesn't seem to be anything obvious in the backend files but the main.js file contains all the information on how the web app handles commands and ultimately the game winning conditions.

Upon initial glance, I come across the function CheckMessage() which handles the command inputs:

```
async function CheckMessage() {
    fetchingResponse = true;
    currentCommand = commandHistory[commandHistory.length - 1];

    if (availableOptions[currentStep].includes(currentCommand) || availableOptions['secret'].includes(currentCommand)) {
        await fetch('/api/monitor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'command': currentCommand })
        })
            .then((res) => res.json())
            .then(async (data) => {
                console.log(data)
                await displayLineInTerminal({ text: data.message });

                if(data.message.includes('Game over')) {
                    playerLost();
                    fetchingResponse = false;
                    return;
                }

                if(data.message.includes('HTB{')) {
                    playerWon();
                    fetchingResponse = false;

                    return;
                }

                if (currentCommand == 'HEAD NORTH') {
                    currentStep = '2';
                }
                else if (currentCommand == 'FOLLOW A MYSTERIOUS PATH') {
                    currentStep = '3'
                }
                else if (currentCommand == 'SET UP CAMP') {
                    currentStep = '4'
                }

                let lineBreak = document.createElement("br");


                beforeDiv.parentNode.insertBefore(lineBreak, beforeDiv);
                displayLineInTerminal({ text: '<span class="command">You have 4 options!</span>' })
                displayLinesInTerminal({ lines: availableOptions[currentStep] })
                fetchingResponse = false;
            });


    }
    else {
        displayLineInTerminal({ text: "You do realise its not a park where you can just play around and move around pick from options how are hard it is for you????" });
        fetchingResponse = false;
    }
}
```

So clearly there is a 'secret' set of commands that isn't provided to the user when they enter "help" for command options.

Looking further into this on the main.js file, I find that the command options are stored in the api directory under options:

```
const fetchOptions = () => {
    fetch('/api/options')
        .then((data) => data.json())
        .then((res) => {
            availableOptions = res.allPossibleCommands;

        })
        .catch(() => {
            availableOptions = undefined;
        })
}
```

Inspecting the /api/options endpoint:




As you can see, there is a secret command: "Blip-blop, in a pickle with a hiccup! Shmiggity-shmack"

#### 3. Using secret command

Armed with the secret command, we can start the game again and enter the command to get the flag:

