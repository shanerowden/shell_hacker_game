// a constant value is being assigned to a new instance of Vanilla Terminal
const term = new VanillaTerminal({
    
    commands: {
        version: (terminal) => {
            terminal.output('Hello and welcome to the corporate onboarding. We see that you have lost access to your SPI adapter. What can you present as a second factor for authorization to this account from this node point?')
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

term.prompt('Your name', (name) => {
    term.output(`Hi ${name}!`);
    term.setPrompt(`${name} `);
});
