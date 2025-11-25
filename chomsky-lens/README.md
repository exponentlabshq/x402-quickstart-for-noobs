# Chomsky Lens

A self-contained, single-file HTML application for color-coding parts of speech in transcripts using the full WordNet dictionary.

## Overview

Chomsky Lens analyzes text and highlights different parts of speech with color coding:
- **Nouns** (blue) - Capitalized words and lowercase words not in other dictionaries
- **Verbs** (green) - From WordNet verb dictionary
- **Adjectives** (red) - From WordNet adjective dictionary
- **Adverbs** (orange) - From WordNet adverb dictionary
- **Prepositions** (purple) - Common prepositions

## Features

✅ **Self-contained** - Single HTML file, no dependencies  
✅ **Full WordNet dictionary** - 29,993 words extracted from NLTK's WordNet  
✅ **Offline-capable** - Works without internet connection  
✅ **No server required** - Open directly in any modern browser  
✅ **Smart noun detection** - Detects capitalized words and common nouns  
✅ **Function word filtering** - Excludes common function words from noun detection  

## Usage

1. Open `chomsky-lens-final.html` in any modern web browser
2. Paste your transcript into the text area
3. Click "Process Transcript" to see color-coded output
4. Click "List All Colored Words" to see all highlighted words by category
5. Click "Clear" to reset

## Dictionary Statistics

The embedded dictionary contains:
- **Verbs**: 8,429 words
- **Adjectives**: 17,863 words
- **Adverbs**: 3,630 words
- **Prepositions**: 71 words
- **Total**: 29,993 words

## Technical Details

### WordNet Integration

The dictionary was extracted from NLTK's WordNet corpus using Python:
- Extracted all verbs, adjectives, and adverbs from WordNet synsets
- Encoded using Base64 with null-byte separators
- Embedded directly in the HTML file

### Noun Detection Logic

1. **Capitalized words** - Any word starting with a capital letter (e.g., "Chapter", "I", "CHAPTER")
2. **Lowercase nouns** - Words not found in verb/adverb/preposition/adjective dictionaries and not in the function words list
3. **Function word exclusion** - Common function words (articles, conjunctions, pronouns, etc.) are excluded even when capitalized

### Performance

- Dictionary lookups use JavaScript `Set` objects for O(1) performance
- Token-based processing prevents HTML tag corruption
- Efficient Base64 encoding keeps file size manageable (~380KB)

## File Structure

```
chomsky-lens/
└── chomsky-lens-final.html  (389KB - self-contained app)
```

## Browser Compatibility

Works in all modern browsers that support:
- ES6 JavaScript (Sets, arrow functions)
- `atob()` for Base64 decoding
- CSS Grid/Flexbox for layout

## Color Scheme

- **Nouns**: `#0066cc` (blue)
- **Verbs**: `#008800` (green)
- **Adverbs**: `#cc6600` (orange)
- **Adjectives**: `#cc0000` (red)
- **Prepositions**: `#9900cc` (purple)

## Notes

- The app processes text token-by-token to avoid breaking HTML tags
- Function words are filtered to prevent false noun detection
- Words must be at least 3 characters to be considered lowercase nouns
- All dictionary lookups are case-insensitive

## License

This is a utility tool for text analysis. The WordNet data is from Princeton University's WordNet project.

