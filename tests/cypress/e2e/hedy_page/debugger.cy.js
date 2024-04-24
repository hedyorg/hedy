describe('Test editor box functionality', () => {

  it('Test echo, print, ask level 1', () => {
    cy.intercept('/parse').as('parse')

    visitLevel(1);

    cy.focused().type('print Hello world\nask Hello!\necho');
    codeMirrorContent().should('have.text', 'print Hello worldask Hello!echo');

    cy.get('#debug_button').click();
    cy.wait('@parse')

    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');

    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', 'Hello world');

    codeMirrorLines()
      .eq(1)
      .should('have.class', 'cm-debugger-current-line');

    cy.get('#debug_continue').click();
    cy.get('#ask-modal').should('be.visible');
    cy.get('#ask-modal > form > div > input[type="text"]').type('Hedy!');
    cy.get('#ask-modal > form > div > input[type="submit"]').click();

    codeMirrorLines()
      .eq(2)
      .should('have.class', 'cm-debugger-current-line');

    cy.get('#debug_continue').click();

    cy.get('#output').should('contain.text', 'Hedy!');
  });

  it('Test is, ask and sleep level 2', () => {
    cy.intercept('/parse').as('parse')
    visitLevel(2);

    cy.focused().type('name is ask What is your name?\nprint Hello name\nage is 15\nprint name is age years old.');

    cy.get('#debug_button').click();
    cy.wait('@parse')

    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');

    cy.get('#debug_continue').click();
    cy.get('#ask-modal').should('be.visible');
    cy.get('#ask-modal > form > div > input[type="text"]').type('Hedy');
    cy.get('#ask-modal > form > div > input[type="submit"]').click();

    codeMirrorLines()
      .eq(1)
      .should('have.class', 'cm-debugger-current-line');

    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', 'Hello Hedy');

    codeMirrorLines()
      .eq(2)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    codeMirrorLines()
      .eq(3)
      .should('have.class', 'cm-debugger-current-line');

    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', 'Hedy is 15 years old.');
  });

  it('Test sleep, clear level 4', () => {
    cy.intercept('/parse').as('parse');
    visitLevel(4);

    cy.focused().type("print '3'\nsleep\nclear");

    cy.get('#debug_button').click();
    cy.wait('@parse')

    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');

    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', '3');

    codeMirrorLines()
      .eq(1)
      .should('have.class', 'cm-debugger-current-line');

    cy.get('#debug_continue').click();
    cy.wait(1000) // next command is sleep so wait 1 second

    codeMirrorLines()
      .eq(2)
      .should('have.class', 'cm-debugger-current-line');

    cy.get('#debug_continue').click();
    cy.get('#output').should('be.empty');
  });

  it('Test if and else level 5, with condition true', () => {
    cy.intercept('/parse').as('parse');

    visitLevel(5);

    cy.focused().type("name is Hedy\nif name is Hedy print 'nice'\nelse print 'boo!'");

    cy.get('#debug_button').click();
    cy.wait('@parse')

    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq('if name is Hedy'.split(' '))
    })
    cy.get('#debug_continue').click();

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq("print 'nice'".split(' '))
    })
    cy.get('#debug_continue').click();
  });

  it('Test if and else level 5, with condition false', () => {
    cy.intercept('/parse').as('parse');

    visitLevel(5);

    cy.focused().type("name is Hedy\nif name is Jesus print 'nice'\nelse print 'boo!'");

    cy.get('#debug_button').click();
    cy.wait('@parse')

    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq('if name is Jesus'.split(' '))
    })
    cy.get('#debug_continue').click();

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq("print 'boo!'".split(' '))
    })
    cy.get('#debug_continue').click();
  });


  it('Test repeat with print statement inside ', () => {
    cy.intercept('/parse').as('parse');

    visitLevel(7);

    cy.focused().type("repeat 3 times print 'Hedy is fun'");

    cy.get('#debug_button').click();
    cy.wait('@parse')

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq("repeat 3 times".split(' '))
    })
    cy.get('#debug_continue').click();


    // For some reason not yet known to me we have to pass two times on a for statement
    // the first time it executes
    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq("repeat 3 times".split(' '))
    })
    cy.get('#debug_continue').click();

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq(['print', "'Hedy is fun'"])
    })
    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', 'Hedy is fun');

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq("repeat 3 times".split(' '))
    })
    cy.get('#debug_continue').click();

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq(['print', "'Hedy is fun'"])
    })
    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', 'Hedy is fun\nHedy is fun');

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq("repeat 3 times".split(' '))
    })
    cy.get('#debug_continue').click();

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq(['print', "'Hedy is fun'"])
    })
    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', 'Hedy is fun\nHedy is fun\nHedy is fun');
  });
  it('Test if with repeat statement inside ', () => {
    cy.intercept('/parse').as('parse');

    visitLevel(7);

    cy.focused().type("if 1 is 1 repeat 1 times print 'Hedy is fun'");
    cy.get('#debug_button').click();
    cy.wait('@parse')

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq('if 1 is 1'.split(' '))
    })
    cy.get('#debug_continue').click();

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq('repeat 1 times'.split(' '))
    })
    cy.get('#debug_continue').click();

    // For some reason not yet known to me we have to pass two times on a for statement
    // the first time it executes
    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq('repeat 1 times'.split(' '))
    })
    cy.get('#debug_continue').click();

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq(['print', "'Hedy is fun'"])
    })
    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', 'Hedy is fun');
  });
  it('Test repeat with blocks', () => {
    cy.intercept('/parse').as('parse');

    visitLevel(8);

    cy.focused().type("repeat 2 times\n    print 'a'\nprint 'b'");
    cy.get('#debug_button').click();
    cy.wait('@parse')

    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    // For some reason not yet known to me we have to pass two times on a for statement
    // the first time it executes
    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    codeMirrorLines()
      .eq(1)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', 'a');

    codeMirrorLines()
      .eq(2)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', 'a\nb');

    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    codeMirrorLines()
      .eq(1)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', 'a\nb\na');

    codeMirrorLines()
      .eq(2)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', 'a\nb\na\nb');
  });

  it('Test if with condition true', () => {
    cy.intercept('/parse').as('parse');

    visitLevel(8);

    cy.focused().type("if Hedy is Hedy\n    print 'Welcome Hedy'");

    cy.get('#debug_button').click();
    cy.wait('@parse')

    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    codeMirrorLines()
      .eq(1)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', 'Welcome Hedy');
  });
  it('Test ifelse with condition false', () => {
    cy.intercept('/parse').as('parse');
    visitLevel(8);

    cy.focused().type("if Jesus is Hedy\n    print 'Welcome Hedy'\n{backspace}else\n    print 'Not Hedy'");

    cy.get('#debug_button').click();
    cy.wait('@parse')

    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    codeMirrorLines()
      .eq(3)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();
    cy.get('#output').should('contain.text', 'Not Hedy');
  });
  it('Test repeat with blocks', () => {
    cy.intercept('/parse').as('parse');

    visitLevel(8);
    cy.focused().type("repeat 1 times\n    turn 3\nforward 50");

    cy.get('#debug_button').click();
    cy.wait('@parse')

    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    // For some reason not yet known to me we have to pass two times on a for statement
    // the first time it executes
    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    codeMirrorLines()
      .eq(1)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    codeMirrorLines()
      .eq(2)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    cy.get('#turtlecanvas').should('be.visible');
  });

  it('Test repeat with ifelse inside', () => {
    cy.intercept('/parse').as('parse');

    visitLevel(9);

    cy.focused().type("repeat 1 times{enter}    if pizza is pizza{enter}    print 'nice!'{enter}{backspace}else\n    print 'pizza is better'");

    cy.get('#debug_button').click();
    cy.wait('@parse')

    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    // For some reason not yet known to me we have to pass two times on a for statement
    // the first time it executes
    codeMirrorLines()
      .eq(0)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    codeMirrorLines()
      .eq(1)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    codeMirrorLines()
      .eq(2)
      .should('have.class', 'cm-debugger-current-line');
    cy.get('#debug_continue').click();

    cy.get('#output').should('contain.text', 'nice!');
  });

  it('Test flat if split between lines', () => {
    cy.intercept('/parse').as('parse');

    visitLevel(5);

    cy.focused().type("if x is y\nprint '!bonito!'\nelse print 'meh'");

    cy.get('#debug_button').click();
    cy.wait('@parse')

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq('if x is y'.split(' '));
    });
    cy.get('#debug_continue').click();

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq(['print', "'meh'"]);
    });

    cy.get('#debug_continue').click();

    cy.get('#output').should('contain.text', 'meh');
  });

  it('Test repeat with flat if split between lines inside', () => {
    cy.intercept('/parse').as('parse');

    visitLevel(7);

    cy.focused().type("repeat 1 times if x is x print 'a'\nelse print 'b'");

    cy.get('#debug_button').click();
    cy.wait('@parse')

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq('repeat 1 times'.split(' '));
    });
    cy.get('#debug_continue').click();

    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq('repeat 1 times'.split(' '));
    });
    cy.get('#debug_continue').click();
    
    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq('if x is x'.split(' '));
    });
    cy.get('#debug_continue').click();
    
    cy.get('.cm-debugger-current-line > span').then(els => {
      const texts = [...els].map(getText);
      expect(texts).to.deep.eq(['print', "'a'"]);
    });

    cy.get('#debug_continue').click();

    cy.get('#output').should('contain.text', 'a');
  });
  
  describe('Test play with no variables', () => {
    for (let i = 1; i <= 10; i++) {
      it ('Test play no variables level ' + i, () => {
        cy.intercept('/parse').as('parse');
        
        visitLevel(i)
        
        cy.focused().type("play C4\nplay D4\nplay E4\n");
    
        cy.get('#debug_button').click();
        cy.wait('@parse')
        
        for (let line = 0; line < 3; line++) {
          codeMirrorLines()
            .eq(line)
            .should('have.class', 'cm-debugger-current-line');
          cy.get('#debug_continue').click();
        }
      })
    }
  })

  describe('Test play with variables', () => {
    for (let i = 2; i <= 11; i++) {
      it ('Test play variables level ' + i, () => {
        cy.intercept('/parse').as('parse');
        
        visitLevel(i)
        
        cy.focused().type("note1 is C4\nnote2 is D4\nnote3 is E4\nplay C4\nplay D4\nplay E4\n");
    
        cy.get('#debug_button').click();
        cy.wait('@parse')

        for (let line = 0; line < 6; line++) {
          codeMirrorLines()
            .eq(line)
            .should('have.class', 'cm-debugger-current-line');
          cy.get('#debug_continue').click();
        }
      })
    }
  })
});

/**
 * Clear the input via sending a whole bunch of {backspace} keystrokes
 *
 * We tried all kinds of `.clear()` invocations, all of them worked on our
 * desktops and never on GitHub Actions. The current invocation does
 * seem to work consistently on GHA, and we collectively have no idea
 * why ¯\_(ツ)_/¯.
 */
function clearViaBackspace() {
  cy.focused().type('{moveToEnd}' + '{backspace}'.repeat(200));
  codeMirrorContent().should('have.text', '');
}

function codeMirrorContent() {
  return cy.get('#editor > .cm-editor > .cm-scroller > .cm-content');
}

function codeMirrorLines() {
  return cy.get('#editor > .cm-editor > .cm-scroller > .cm-content > .cm-line');
}

function checkFullDebugLine(lineHeight, line) {
  cy.get('.debugger-current-line')
    .invoke('attr', 'style')
    .then((text) => {
      const topRe = new RegExp('top: ([0-9]+(.[0-9]*)?)+px', 'gu');
      cy.log(text)
      const matches = topRe.exec(text);
      const lineTop = parseFloat(matches[1]);
      expect(lineTop).to.eq(lineHeight * (line - 1));
    });
}

function checkPartialDebugLine(lineHeight, line, begginingOfLine) {
  cy.get('.debugger-current-line')
    .invoke('attr', 'style')
    .then((text) => {
      cy.log(text)
      const topRe = new RegExp('top: ([0-9]+(.[0-9]*)?)+px', 'gu');
      let matches = topRe.exec(text);
      const lineTop = parseFloat(matches[1]);
      expect(lineTop).to.eq(lineHeight * (line - 1));

      const leftRe = new RegExp('left: ([0-9]+(.[0-9]+)?)+px', 'gu');
      matches = leftRe.exec(text);
      const leftVal = parseFloat(matches[1]);
      if (begginingOfLine) {
        expect(leftVal).to.eq(4)
      } else {
        expect(leftVal).to.be.greaterThan(4)
      }
    });
}

function visitLevel(level) {
  cy.visit(`${Cypress.env('hedy_page')}/${level}#default`);
  codeMirrorContent().click();
  cy.focused().clear();
}

const getText = el => el.textContent.trim();