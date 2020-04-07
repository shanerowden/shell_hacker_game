// a constant value is being assigned to a new instance of Vanilla Terminal
const term = new VanillaTerminal({
    
    commands: {
        dicks: (terminal) => {
            terminal.output('Hello and welcome to the corporate onboarding. We see that you have lost access to your secure ')
            terminal.setPrompt('@soyjavi <small>❤️</small> <u>vanilla</u> ');
        },

        async: (terminal) => {
            terminal.idle();
            setTimeout(() => terminal.output('Async 300'), 300);
            setTimeout(() => terminal.output('Async 1300'), 1300);
            setTimeout(() => {
            terminal.output('Async 2000');
            terminal.setPrompt();
            }, 2000);
        },
        },

        // welcome: 'Welcome...',
        // prompt: 'soyjavi at <u>Macbook-Pro</u> ',
        separator: '$',
    });

term.onInput((command, parameters) => {
    console.log('⚡️onInput', command, parameters);
});

let hashword = "correct";
let guess = "wrong";

    

// term.prompt('GIDC Zeon v4.8 SiC<br>box7xCd login', (user) => {
//     term.output();
//     do { 
//         term.prompt('hashword:', (hashword) => {
//             term.output('Are you ${user}?<br>Try again.');
//         }); 
//     } while (guess != hashword);
// });
// term.setPrompt('GIDC Zeon v4.8 SiC<br>box7xCd login');

// 




term.prompt('Your name', (name) => {
    term.output(`Hi ${name}!`);
    term.setPrompt(`${name} `);
});
