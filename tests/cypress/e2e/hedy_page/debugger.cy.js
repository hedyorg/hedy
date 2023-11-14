describe('Test editor box functionality', () => {
  it('Test echo, print, ask level 1', () => {
    const heightRe = new RegExp('height: ([0-9]+(.[0-9]+)?)+px', 'gu');    
    visitLevel(1)
    cy.focused().type('print Hello world\nask Hello!\necho');
    
    cy.get('.ace_active-line').invoke('attr', 'style').then((text) => {
      // We calculate the height of the lines to later get the active line
      const matches = heightRe.exec(text);
      const lineHeight = parseFloat(matches[1]);
      aceContent().should('have.text', 'print Hello worldask Hello!echo');
      cy.get('#debug_button').click();

      // checkFullDebugLine(lineHeight, 1);
      cy.get('#debug_continue').click();
      cy.get('#output').should('contain.text', 'Hello world');

      // checkFullDebugLine(lineHeight, 2);
      cy.get('#debug_continue').click();
      cy.get('#ask-modal').should('be.visible');
      cy.get('#ask-modal > form > div > input[type="text"]').type('Hedy!');
      cy.get('#ask-modal > form > div > input[type="submit"]').click();

      // checkFullDebugLine(lineHeight, 3)
      cy.get('#debug_continue').click();
      cy.get('#output').should('contain.text', 'Hedy!');
      cy.wait(1000)
      // cy.get('#debug_button').should('be.visible'); // we finished execution
    });
  });
  
  it('Test is, ask and sleep level 2', () => {
    const heightRe = new RegExp('height: ([0-9]+(.[0-9]+)?)+px', 'gu');    
    visitLevel(2);
    cy.focused().type('name is ask What is your name?\nprint Hello name\nage is 15\nprint name is age years old.');
    
    cy.get('.ace_active-line').invoke('attr', 'style').then((text) => {
      // We calculate the height of the lines to later get the active line
      const matches = heightRe.exec(text);
      const lineHeight = parseFloat(matches[1]);
      cy.get('#debug_button').click();    
      
      // checkFullDebugLine(lineHeight, 1);
      cy.get('#debug_continue').click();
      cy.get('#ask-modal').should('be.visible');
      cy.get('#ask-modal > form > div > input[type="text"]').type('Hedy');
      cy.get('#ask-modal > form > div > input[type="submit"]').click();
      
      // checkFullDebugLine(lineHeight, 2);
      cy.get('#debug_continue').click();    
      cy.get('#output').should('contain.text', 'Hello Hedy');
      
      // checkFullDebugLine(lineHeight, 3);
      cy.get('#debug_continue').click();    
      
      // checkFullDebugLine(lineHeight, 4);
      cy.get('#debug_continue').click();    
      cy.get('#output').should('contain.text', 'Hedy is 15 years old.'); 
      cy.wait(1000)
      // cy.get('#debug_button').should('be.visible'); // we finished execution
    });
  });

  it('Test sleep, clear level 4', () => {
    const heightRe = new RegExp('height: ([0-9]+(.[0-9]+)?)+px', 'gu');    
    visitLevel(4);
    cy.focused().type("print '3'\nsleep\nclear");
    
    cy.get('.ace_active-line').invoke('attr', 'style').then((text) => {
      // We calculate the height of the lines to later get the active line
      const matches = heightRe.exec(text);
      const lineHeight = parseFloat(matches[1]);
      cy.get('#debug_button').click();    
      
      // checkFullDebugLine(lineHeight, 1);
      cy.get('#debug_continue').click();
      cy.get('#output').should('contain.text', '3');
      
      // checkFullDebugLine(lineHeight, 2);
      cy.get('#debug_continue').click();    
      cy.wait(1000) // next command is sleep so wait 1 second
      
      // checkFullDebugLine(lineHeight, 3);
      cy.get('#debug_continue').click();
      cy.get('#output').should('be.empty');
      cy.wait(1000)
      // cy.get('#debug_button').should('be.visible'); // we finished execution
    });
  });

  it('Test if and else level 5, with condition true', () => {
    const heightRe = new RegExp('height: ([0-9]+(.[0-9]+)?)+px', 'gu');  
        
    visitLevel(5);
    cy.focused().type("name is Hedy\nif name is Hedy print 'nice'\nelse print 'boo!'");
    
    cy.get('.ace_active-line').invoke('attr', 'style').then((text) => {
      // We calculate the height of the lines to later get the active line
      const matches = heightRe.exec(text);
      const lineHeight = parseFloat(matches[1]);
      cy.get('#debug_button').click();    

      // checkFullDebugLine(lineHeight, 1);      
      cy.get('#debug_continue').click();
      
      //checkPartialDebugLine(lineHeight, 2, true);
      cy.get('#debug_continue').click();

      //checkPartialDebugLine(lineHeight, 2, false);
      cy.get('#debug_continue').click();
      cy.wait(1000)
      
      // The else should not be highlighter and we stop execution
      // cy.get('#debug_button').should('be.visible'); // we finished execution
    });
  });

  it('Test if and else level 5, with condition false', () => {
    const heightRe = new RegExp('height: ([0-9]+(.[0-9]+)?)+px', 'gu');  
        
    visitLevel(5);
    cy.focused().type("name is Hedy\nif name is Jesus print 'nice'\nelse print 'boo!'");
    
    cy.get('.ace_active-line').invoke('attr', 'style').then((text) => {
      // We calculate the height of the lines to later get the active line
      const matches = heightRe.exec(text);
      const lineHeight = parseFloat(matches[1]);
      cy.get('#debug_button').click();    

      // checkFullDebugLine(lineHeight, 1);      
      cy.get('#debug_continue').click();
      
      //checkPartialDebugLine(lineHeight, 2, true);
      cy.get('#debug_continue').click();

      // we should highlight the print statement after the else!
      //checkPartialDebugLine(lineHeight, 3, false);
      cy.get('#debug_continue').click();
      cy.wait(1000)
      
      // The else should not be highlighter and we stop execution
      // cy.get('#debug_button').should('be.visible'); // we finished execution
    });
  });

  it('Test repeat with print statement inside ', () => {
    const heightRe = new RegExp('height: ([0-9]+(.[0-9]+)?)+px', 'gu');  
        
    visitLevel(7);
    cy.focused().type("repeat 3 times print 'Hedy is fun'");
    
    cy.get('.ace_active-line').invoke('attr', 'style').then((text) => {
      // We calculate the height of the lines to later get the active line
      const matches = heightRe.exec(text);
      const lineHeight = parseFloat(matches[1]);
      
      cy.get('#debug_button').click();
      
      //checkPartialDebugLine(lineHeight, 1, true);
      cy.get('#debug_continue').click();
      
      // For some reason not yet known to me we have to pass two times on a for statement
      // the first time it executes
      //checkPartialDebugLine(lineHeight, 1, true);
      cy.get('#debug_continue').click();

      //checkPartialDebugLine(lineHeight, 1, false);
      cy.get('#debug_continue').click();
      cy.get('#output').should('contain.text', 'Hedy is fun');

      //checkPartialDebugLine(lineHeight, 1, true);
      cy.get('#debug_continue').click();
      
      //checkPartialDebugLine(lineHeight, 1, false);
      cy.get('#debug_continue').click();
      cy.get('#output').should('contain.text', 'Hedy is fun\nHedy is fun');
      
      //checkPartialDebugLine(lineHeight, 1, true);
      cy.get('#debug_continue').click();

      //checkPartialDebugLine(lineHeight, 1, false);
      cy.get('#debug_continue').click();
      cy.get('#output').should('contain.text', 'Hedy is fun\nHedy is fun\nHedy is fun');
      cy.wait(1000)
            
      // cy.get('#debug_button').should('be.visible'); // we finished execution
    });
  });

  it('Test repeat with if statement inside ', () => {
    const heightRe = new RegExp('height: ([0-9]+(.[0-9]+)?)+px', 'gu');  
        
    visitLevel(7);
    cy.focused().type("if 1 is 1 repeat 1 times print 'Hedy is fun'");
    
    cy.get('.ace_active-line').invoke('attr', 'style').then((text) => {
      // We calculate the height of the lines to later get the active line
      const matches = heightRe.exec(text);
      const lineHeight = parseFloat(matches[1]);
      
      cy.get('#debug_button').click();
      
      //checkPartialDebugLine(lineHeight, 1, true);
      cy.get('#debug_continue').click();

      //checkPartialDebugLine(lineHeight, 1, false);
      cy.get('#debug_continue').click();

      // For some reason not yet known to me we have to pass two times on a for statement
      // the first time it executes
      //checkPartialDebugLine(lineHeight, 1, false);
      cy.get('#debug_continue').click();

      //checkPartialDebugLine(lineHeight, 1, false);
      cy.get('#debug_continue').click();
      cy.get('#output').should('contain.text', 'Hedy is fun');
      cy.wait(1000)
          
      // cy.get('#debug_button').should('be.visible'); // we finished execution
    });
  });

  it('Test repeat with blocks', () => {
    const heightRe = new RegExp('height: ([0-9]+(.[0-9]+)?)+px', 'gu');  
        
    visitLevel(8);
    cy.focused().type("repeat 2 times\n    print 'a'\nprint 'b'");
    
    cy.get('.ace_active-line').invoke('attr', 'style').then((text) => {
      // We calculate the height of the lines to later get the active line
      const matches = heightRe.exec(text);
      const lineHeight = parseFloat(matches[1]);
      
      cy.get('#debug_button').click();
      
      // checkFullDebugLine(lineHeight, 1);
      cy.get('#debug_continue').click();
      
      // For some reason not yet known to me we have to pass two times on a for statement
      // the first time it executes
      // checkFullDebugLine(lineHeight, 1);
      cy.get('#debug_continue').click();
      
      // checkFullDebugLine(lineHeight, 2);
      cy.get('#debug_continue').click();      
      cy.get('#output').should('contain.text', 'a');
      
      // checkFullDebugLine(lineHeight, 3);
      cy.get('#debug_continue').click();      
      cy.get('#output').should('contain.text', 'a\nb');

      // checkFullDebugLine(lineHeight, 1);
      cy.get('#debug_continue').click();
      
      // checkFullDebugLine(lineHeight, 2);
      cy.get('#debug_continue').click();      
      cy.get('#output').should('contain.text', 'a\nb\na');
      
      // checkFullDebugLine(lineHeight, 3);
      cy.get('#debug_continue').click();      
      cy.get('#output').should('contain.text', 'a\nb\na\nb');
      cy.wait(1000)
            
      // cy.get('#debug_button').should('be.visible'); // we finished execution
    });
  });

  it('Test if with condition true', () => {
    const heightRe = new RegExp('height: ([0-9]+(.[0-9]+)?)+px', 'gu');  
        
    visitLevel(8);
    cy.focused().type("if Hedy is Hedy\n    print 'Welcome Hedy'");
    
    cy.get('.ace_active-line').invoke('attr', 'style').then((text) => {
      // We calculate the height of the lines to later get the active line
      const matches = heightRe.exec(text);
      const lineHeight = parseFloat(matches[1]);
      
      cy.get('#debug_button').click();
      
      // checkFullDebugLine(lineHeight, 1);
      cy.get('#debug_continue').click();
        
      // checkFullDebugLine(lineHeight, 2);
      cy.get('#debug_continue').click();      
      cy.get('#output').should('contain.text', 'Welcome Hedy');
      cy.wait(1000)
            
      // cy.get('#debug_button').should('be.visible'); // we finished execution
    });
  });

  it('Test ifelse with condition false', () => {
    const heightRe = new RegExp('height: ([0-9]+(.[0-9]+)?)+px', 'gu');  
        
    visitLevel(8);
    cy.focused().type("if Jesus is Hedy\n    print 'Welcome Hedy'\n{backspace}else\n    print 'Not Hedy'");
    
    cy.get('.ace_active-line').invoke('attr', 'style').then((text) => {
      // We calculate the height of the lines to later get the active line
      const matches = heightRe.exec(text);
      const lineHeight = parseFloat(matches[1]);
      
      cy.get('#debug_button').click();
      
      // checkFullDebugLine(lineHeight, 1);
      cy.get('#debug_continue').click();
        
      // checkFullDebugLine(lineHeight, 4);
      cy.get('#debug_continue').click();      
      cy.get('#output').should('contain.text', 'Not Hedy');
      cy.wait(1000)
            
      // cy.get('#debug_button').should('be.visible'); // we finished execution
    });
  });

  it('Test repeat with blocks', () => {
    const heightRe = new RegExp('height: ([0-9]+(.[0-9]+)?)+px', 'gu');  

    visitLevel(8);
    cy.focused().type("repeat 1 times\n    turn 3\nforward 50");
    
    cy.get('.ace_active-line').invoke('attr', 'style').then((text) => {
      // We calculate the height of the lines to later get the active line
      const matches = heightRe.exec(text);
      const lineHeight = parseFloat(matches[1]);
      
      cy.get('#debug_button').click();
      
      // checkFullDebugLine(lineHeight, 1);
      cy.get('#debug_continue').click();
      
      // For some reason not yet known to me we have to pass two times on a for statement
      // the first time it executes
      // checkFullDebugLine(lineHeight, 1);
      cy.get('#debug_continue').click();
      
      // checkFullDebugLine(lineHeight, 2);
      cy.get('#debug_continue').click();
      
      // checkFullDebugLine(lineHeight, 3);
      cy.get('#debug_continue').click(); 

      cy.get('#turtlecanvas').should('be.visible'); 
      cy.wait(1000)
      // cy.get('#debug_button').should('be.visible'); // we finished execution
    });
  });

  it('Test repeat with ifelse inside', () => {
    const heightRe = new RegExp('height: ([0-9]+(.[0-9]+)?)+px', 'gu');  

    visitLevel(9);
    cy.focused().type("repeat 1 times\n    if pizza is pizza\n    print 'nice!'\n{backspace}else\n    print 'pizza is better'");
    
    cy.get('.ace_active-line').invoke('attr', 'style').then((text) => {
      // We calculate the height of the lines to later get the active line
      const matches = heightRe.exec(text);
      const lineHeight = parseFloat(matches[1]);
      
      cy.get('#debug_button').click();
      
      // checkFullDebugLine(lineHeight, 1);
      cy.get('#debug_continue').click();
      
      // For some reason not yet known to me we have to pass two times on a for statement
      // the first time it executes
      // checkFullDebugLine(lineHeight, 1);
      cy.get('#debug_continue').click();
      
      // checkFullDebugLine(lineHeight, 2);
      cy.get('#debug_continue').click();
      
      // checkFullDebugLine(lineHeight, 3);
      cy.get('#debug_continue').click(); 

      cy.get('#output').should('contain.text', 'nice!');
      cy.wait(1000)

      // cy.get('#debug_button').should('be.visible'); // we finished execution
    });
  });
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
  aceContent().should('have.text', '');
}

function aceContent() {
  return cy.get('#editor > .ace_scroller > .ace_content');
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
  aceContent().click();
  clearViaBackspace();
}