import { EditorView, basicSetup} from "codemirror"
import { keymap, placeholder, ViewUpdate } from "@codemirror/view"
import { php } from "@codemirror/lang-php"
import { html } from "@codemirror/lang-html"
import { css } from "@codemirror/lang-css"
import { javascript } from "@codemirror/lang-javascript"
import { EditorState } from "@codemirror/state";
import { oneDark } from "@codemirror/theme-one-dark"
import { defaultKeymap, historyKeymap, indentWithTab } from "@codemirror/commands";
import { indentUnit } from "@codemirror/language"
import { completionKeymap, currentCompletions } from "@codemirror/autocomplete";

class Base {
	#extensions = [];
	#options	= {};
	
	constructor(extensions, options = {}) {
		for (const extension of extensions) {
			this.#extensions.push(extension);
		}
		this.#options = options;
	}

	newState(content, options = {}) {
		const extensions = this.#extensions.slice();

		if ('placeholder' in options) {
			extensions.push(placeholder(options.placeholder));
		}

		if ('focus' in options) {
			extensions.push(EditorView.updateListener.of((event) => {
				if (event.focusChanged) {
					options.focus.value = event.view.state.doc.toString();
				}
			}));
		}
		
		if ('change' in options && typeof options.change === 'function') {
			extensions.push(EditorView.updateListener.of((v) => {
				if(v.docChanged){
					options.change();
				}
			}))
		}

		if ('styles' in options) {
			extensions.push(EditorView.theme(options.styles))
		}

		if (options.lineWrapping ?? true){
			extensions.push(EditorView.lineWrapping);
		}

		if ('save_keymap' in options){
			extensions.push(keymap.of([options.save_keymap]))
		}
		
		if ('extensions' in this.#options && typeof(this.#options.extensions) === 'object') {
			for (const [name, extension] of Object.entries(this.#options.extensions)) {
				if (name in options && options[name] === true) {
					extensions.push(extension);
				}
			}
		}


		return EditorState.create({
			doc:		content,
			extensions:	extensions,
		});
	}

	newView(element, state, options = {}) {		
		return new EditorView(Object.assign({}, {
			parent: element,
			state, 
		}));
	}

	newEditor(element, content, options = {}) {
		const state = this.newState(content, options);
		
		return this.newView(element, state, options);
	}

	fromElement(element, options = {}) {
		if (element.nodeName === 'TEXTAREA') {
			return this.#textarea(element, options);
		}

		const content = element.innerHTML;
		element.innerHTML = '';
		return this.newEditor(element, content, options);
	}

	textarea(element, options = {}) {
		return this.fromElement(element, options);
	}

	#textarea(textarea, options = {}) {
		const placeholder = textarea.getAttribute('placeholder');
		if (placeholder && placeholder.length) {
			options.placeholder = placeholder;
		}

		options.focus = textarea;
		
		const element		= document.createElement('div');
		element.className	= 'codemirror';
		const view			= this.newEditor(element, textarea.value, options);

		textarea.parentNode.insertBefore(element, textarea);
		textarea.style.display = 'none';
		if (textarea.form) {
			textarea.form.addEventListener('submit', () => {
				textarea.value = view.state.doc.toString();
			});
		}

		return view;
	}
}

// Extensions included this way are always loaded
const extensions = [
  basicSetup, 
  php(),
  html(),
  javascript(),
  css(),
  indentUnit.of("    "),
  keymap.of([
    indentWithTab,
    ...defaultKeymap,
    ...completionKeymap,
    ...historyKeymap,
  ]),
];

// Extensions included this way can be loaded if the relevant option name is passed to the initialisation script with a boolean value - see custom js example file
const options = {
  extensions: {
    dark: oneDark
  },
}

export function load() {
  return new Base(extensions, options);
}