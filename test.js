Object.defineProperty(exports, "__esModule", {value: true});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _modules = __webpack_require__(/*! ./modules */ "./src/modules/index.js");

var _VanillaTerminal = __webpack_require__(/*! ./VanillaTerminal.css */ "./src/VanillaTerminal.css");

var _VanillaTerminal2 = _interopRequireDefault(_VanillaTerminal);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _toArray(arr) { return Array.isArray(arr) ? arr : Array.from(arr); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

// eslint-disable-line

var KEY = 'VanillaTerm';

var _window = window,
    addEventListener = _window.addEventListener,
    localStorage = _window.localStorage;

var Terminal = function () {
  function Terminal() {
    var props = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};

    _classCallCheck(this, Terminal);

    _initialiseProps.call(this);

    var _props$container = props.container,
        container = _props$container === undefined ? 'vanilla-terminal' : _props$container,
        _props$commands = props.commands,
        commands = _props$commands === undefined ? {} : _props$commands,
        _props$welcome = props.welcome,
        welcome = _props$welcome === undefined ? 'Welcome to <a href="">Vanilla</a> terminal.' : _props$welcome,
        _props$prompt = props.prompt,
        prompt = _props$prompt === undefined ? '' : _props$prompt,
        _props$separator = props.separator,
        separator = _props$separator === undefined ? '&gt;' : _props$separator;

    this.commands = Object.assign({}, commands, _modules.COMMANDS);
    this.history = localStorage[KEY] ? JSON.parse(localStorage[KEY]) : [];
    this.historyCursor = this.history.length;
    this.welcome = welcome;
    this.shell = { prompt: prompt, separator: separator };

    var el = document.getElementById(container);
    if (el) {
      this.cacheDOM(el);
      this.addListeners();
      if (welcome) this.output(welcome);
    } else throw Error('Container #' + container + ' doesn\'t exists.');
  }

  _createClass(Terminal, [{
    key: 'clear',
    value: function clear() {
      this.DOM.output.innerHTML = '';
      this.resetCommand();
    }
  }, {
    key: 'idle',
    value: function idle() {
      var DOM = this.DOM;


      DOM.command.classList.add('idle');
      DOM.prompt.innerHTML = '<div class="spinner"></div>';
    }
  }, {
    key: 'prompt',
    value: function prompt(_prompt) {
      var callback = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : function () {};

      this.state.prompt = true;
      this.onAskCallback = callback;
      this.DOM.prompt.innerHTML = _prompt + ':';
      this.resetCommand();
      this.DOM.command.classList.add('input');
    }
  }, {
    key: 'onInput',
    value: function onInput(callback) {
      this.onInputCallback = callback;
    }
  }, {
    key: 'output',
    value: function output() {
      var html = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '&nbsp;';

      this.DOM.output.insertAdjacentHTML('beforeEnd', '<span>' + html + '</span>');
      this.resetCommand();
    }
  }, {
    key: 'setPrompt',
    value:/*  */ function setPrompt() {
      var prompt = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : this.shell.prompt;
      var DOM = this.DOM,
          separator = this.shell.separator;


      this.shell = { prompt: prompt, separator: separator };
      DOM.command.classList.remove('idle');
      DOM.prompt.innerHTML = '' + prompt + separator;
      DOM.input.focus();
    }
  }]);

  return Terminal;
}();

var _initialiseProps = function _initialiseProps() {
  var _this = this;

  this.state = {
    prompt: undefined,
    idle: undefined
  };

  this.cacheDOM = function (el) {
    el.classList.add(KEY);
    el.insertAdjacentHTML('beforeEnd', (0, _modules.markup)(_this));

    // Cache DOM nodes
    var container = el.querySelector('.container');
    _this.DOM = {
      container: container,
      output: container.querySelector('output'),
      command: container.querySelector('.command'),
      input: container.querySelector('.command .input'),
      prompt: container.querySelector('.command .prompt')
    };
  };

  this.addListeners = function () {
    var DOM = _this.DOM;

    DOM.output.addEventListener('DOMSubtreeModified', function () {
      setTimeout(function () {
        return DOM.input.scrollIntoView();
      }, 10);
    }, false);

    addEventListener('click', function () {
      return DOM.input.focus();
    }, false);
    DOM.output.addEventListener('click', function (event) {
      return event.stopPropagation();
    }, false);
    DOM.input.addEventListener('keyup', _this.onKeyUp, false);
    DOM.input.addEventListener('keydown', _this.onKeyDown, false);
    DOM.command.addEventListener('click', function () {
      return DOM.input.focus();
    }, false);

    addEventListener('keyup', function (event) {
      DOM.input.focus();
      event.stopPropagation();
      event.preventDefault();
    }, false);
  };

  this.onKeyUp = function (event) {
    var keyCode = event.keyCode;
    var DOM = _this.DOM,
        _history = _this.history,
        history = _history === undefined ? [] : _history,
        historyCursor = _this.historyCursor;


    if (keyCode === 27) {
      // ESC key
      DOM.input.value = '';
      event.stopPropagation();
      event.preventDefault();
    } else if ([38, 40].includes(keyCode)) {
      if (keyCode === 38 && historyCursor > 0) _this.historyCursor -= 1; // {38} UP key
      if (keyCode === 40 && historyCursor < history.length - 1) _this.historyCursor += 1; // {40} DOWN key

      if (history[_this.historyCursor]) DOM.input.value = history[_this.historyCursor];
    }
  };

  this.onKeyDown = function (_ref) {
    var keyCode = _ref.keyCode;
    var _commands = _this.commands,
        commands = _commands === undefined ? {} : _commands,
        DOM = _this.DOM,
        history = _this.history,
        onInputCallback = _this.onInputCallback,
        state = _this.state;

    var commandLine = DOM.input.value.trim();
    if (keyCode !== 13 || !commandLine) return;

    var _commandLine$split = commandLine.split(' '),
        _commandLine$split2 = _toArray(_commandLine$split),
        command = _commandLine$split2[0],
        parameters = _commandLine$split2.slice(1);

    if (state.prompt) {
      state.prompt = false;
      _this.onAskCallback(command);
      _this.setPrompt();
      _this.resetCommand();
      return;
    }

    // Save command line in history
    history.push(commandLine);
    localStorage[KEY] = JSON.stringify(history);
    _this.historyCursor = history.length;

    // Clone command as a new output line
    DOM.output.appendChild((0, _modules.cloneCommandNode)(DOM.command));

    // Clean command line
    DOM.command.classList.add('hidden');
    DOM.input.value = '';

    // Dispatch command
    if (Object.keys(commands).includes(command)) {
      var callback = commands[command];
      if (callback) callback(_this, parameters);
      if (onInputCallback) onInputCallback(command, parameters);
    } else {
      _this.output('<u>' + command + '</u>: command not found.');
    }
  };

  this.resetCommand = function () {
    var DOM = _this.DOM;


    DOM.input.value = '';
    DOM.command.classList.remove('input');
    DOM.command.classList.remove('hidden');
    if (DOM.input.scrollIntoView) DOM.input.scrollIntoView();
  };
};

if (window) window.VanillaTerminal = Terminal;

exports.default = Terminal;

//# sourceURL=webpack:///./src/VanillaTerminal.js?"
