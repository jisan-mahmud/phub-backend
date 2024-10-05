from pygments import lexers

def detect_language(snippet):
    """
    Detect the programming language of a given code snippet.
    """
    # Iterate over all available lexers
    for lexer in lexers.get_all_lexers():
        lexer_name, aliases, filenames, mimetypes = lexer
        try:
            # Use the lexer to analyze the snippet
            if lexers.get_lexer_by_name(lexer_name).analyse(snippet):
                return lexer_name  # Return the detected language name
        except Exception:
            continue
    return "unknown"  # Return 'unknown' if no language is detected
