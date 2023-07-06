/**
 * A manager for markers in Ace
 *
 * Some markers need to be cleared upon editing, others not,
 * so this remembers information about the markers.
 */
export class Markers {
  private markerClasses = new Map<number, string>();

  // Map line numbers to markers
  private strikeMarkers = new Map<number, number>();

  private currentLineMarker?: MarkerLocation;

  constructor(private readonly editor: AceAjax.Editor) {
  }

  /**
   * Mark an error location in the ace editor
   *
   * The error occurs at the given row, and optionally has a column and
   * and a length.
   *
   * If 'col' is not given, the entire line will be highlighted red. Otherwise
   * the character at 'col' will be highlighted, optionally extending for
   * 'length' characters.
   *
   * 'row' and 'col' are 1-based.
   */
  public highlightAceError(row: number, col?: number) {
    // Set a marker on the error spot, either a fullLine or a text
    // class defines the related css class for styling; which is fixed in styles.css with Tailwind
    if (col === undefined) {
      // If the is no column, highlight the whole row
      this.addMarker(
        new ace.Range(row - 1, 1, row - 1, 2),
        "editor-error", "fullLine"
      );
      return;
    }
    // If we get here we know there is a column -> dynamically get the length of the error string
    // As we assume the error is supposed to target a specific word we get row[column, whitespace].
    const length = this.editor.session.getLine(row -1).slice(col-1).split(/(\s+)/)[0].length;

    // If there is a column, only highlight the relevant text
    this.addMarker(new ace.Range(row - 1, col - 1, row - 1, col - 1 + length),
      "editor-error", "text"
    );
  }

  /**
   * Remove all error markers
   */
  public clearErrors() {
    for (const marker of this.findMarkers('editor-error')) {
      this.removeMarker(marker);
    }
  }

  /**
   * Remove all incorrect lines markers
   */
  public clearIncorrectLines() {
    const markers = this.editor.session.getMarkers(true);

    if (markers) {
      for (const index in markers) {
        let marker = markers[index];
        if (marker.clazz.includes('ace_incorrect_hedy_code')){
          this.removeMarker(Number(index));
        }
      }
    }
  }

  /**
   * Set the current line in the debugger
   */
  public setDebuggerCurrentLine(line: number | undefined) {
    if (this.currentLineMarker?.line === line) {
      return;
    }

    if (this.currentLineMarker) {
      this.removeMarker(this.currentLineMarker.id);
    }

    if (line === undefined) {
      this.currentLineMarker = undefined;
      return;
    }

    const id = this.addMarker(new ace.Range(line, 0, line, 999), 'debugger-current-line', 'fullLine');
    this.currentLineMarker = { line, id };
  }

  /**
   * Mark the given set of lines as currently struck through
   */
  public strikethroughLines(lines: number[]) {
    const struckLines = new Set(lines);

    // First remove all markers that are no longer in the target set
    const noLongerStruck = Array.from(this.strikeMarkers.entries())
      .filter(([line, _]) => !struckLines.has(line))
    for (const [line, id] of noLongerStruck) {
      this.removeMarker(id);
      this.strikeMarkers.delete(line);
    }

    // Then add markers for lines need to be struck
    const newlyStruck = lines
      .filter(line => !this.strikeMarkers.has(line));
    for (const line of newlyStruck) {
      const id = this.addMarker(new ace.Range(line, 0, line, 999), 'disabled-line', 'text', true);
      this.strikeMarkers.set(line, id);
    }
  }

  /**
   * Add a marker and remember the class
   */
  public addMarker(range: AceAjax.Range, klass: string, scope: 'text' | 'line' | 'fullLine', inFront = false) {
    const id = this.editor.session.addMarker(range, klass, scope, inFront);
    this.markerClasses.set(id, klass);
    return id;
  }

  private removeMarker(id: number) {
    this.editor.session.removeMarker(id);
    this.markerClasses.delete(id);
  }

  private findMarkers(klass: string) {
    return Array.from(this.markerClasses.entries())
      .filter(([_, k]) => k === klass)
      .map(([id, _]) => id);
  }
}

interface MarkerLocation {
  readonly line: number;
  readonly id: number;
}
