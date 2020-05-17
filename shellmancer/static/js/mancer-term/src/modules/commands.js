import PKG from '../../package.json';
import MAN from './help';

const { localStorage } = window;
const KEY = 'MancerTerminal';

export default {
  clear: terminal => terminal.clear(),

  man: (terminal, [command]) => {
    if (command) {
      terminal.output(`man: ${MAN[command] || `no manual entry for <u>${command}</u>`}`);
    } else {
      terminal.output(
        `man is the system's manual pager.  Each page argument given to man is normally the name 
        of a program, utility or function.   The  manual page  associated with each of these arguments
        is then found and displayed.  A section, if provided, will direct man to look only in that section 
        of the manual. The default action is to search in all of the available sections following a 
        pre-defined order ("1 n  l  8  3  23posix  3pm  3perl  3am  5 4 9 6 7" by default, unless 
        overridden by the SECTION directive in /etc/manpath.config), and to show only the first page 
        found, even if page exists in several sections.`,
      );

      terminal.output('Type <u>help name</u> to find out more about the function <u>name</u>.');
      terminal.output(Object.keys(terminal.commands).join(', '));
    }
  },

  version: terminal => terminal.output(`MancerTerminal v${PKG.version} -- fork of vanilla-terminal`),

  wipe: (terminal) => {
    terminal.prompt('Are you sure remove all your commands history? Y/N', (value) => {
      if (value.trim().toUpperCase() === 'Y') {
        localStorage.removeItem(KEY);
        terminal.history = []; // eslint-disable-line
        terminal.historyCursor = 0; // eslint-disable-line
        terminal.output('Command History Log Truncated');
      }
    });
  },
};
