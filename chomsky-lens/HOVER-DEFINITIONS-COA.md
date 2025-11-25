# Courses of Action: Hover Definitions & Wikipedia Summaries

## Overview
Add interactive hover tooltips that display word definitions or Wikipedia summaries when users hover over highlighted words in the Chomsky Lens.

---

## Approach 1: Free Dictionary API (dictionaryapi.dev)

### How it works:
- Use the free, no-auth Dictionary API: `https://api.dictionaryapi.dev/api/v2/entries/en/{word}`
- On hover, fetch definition and display in a modal/tooltip
- Cache results in browser localStorage to avoid repeated API calls

### Pros:
✅ **Free** - No API key required  
✅ **Simple** - Straightforward REST API  
✅ **Fast** - Good response times  
✅ **Reliable** - Public service, well-maintained  
✅ **Definitions** - Provides multiple definitions, phonetic info, examples  

### Cons:
❌ **Rate limiting** - May have limits on requests  
❌ **Network required** - Won't work offline  
❌ **Limited coverage** - May not have all words (especially slang, proper nouns)  

### Implementation complexity: **Low**
- Simple fetch() call
- Basic modal/tooltip UI
- localStorage caching

---

## Approach 2: Wikipedia API (MediaWiki)

### How it works:
- Use Wikipedia's REST API: `https://en.wikipedia.org/api/rest_v1/page/summary/{word}`
- Fetch article summary/extract on hover
- Cache results in localStorage

### Pros:
✅ **Free** - No API key required  
✅ **Comprehensive** - Covers proper nouns, places, concepts, people  
✅ **Rich content** - Provides context, history, related info  
✅ **Images** - Can include thumbnail images  
✅ **Reliable** - Wikipedia infrastructure  

### Cons:
❌ **Network required** - Won't work offline  
❌ **Slower** - Wikipedia API can be slower than dictionary APIs  
❌ **Overkill for simple words** - "the", "and", etc. don't need Wikipedia  
❌ **May not find matches** - Some words won't have Wikipedia articles  

### Implementation complexity: **Low-Medium**
- Simple fetch() call
- Need to handle "not found" cases gracefully
- Modal/tooltip UI

---

## Approach 3: Hybrid Approach (Dictionary + Wikipedia Fallback)

### How it works:
1. On hover, first try Dictionary API for definition
2. If no result or word is a proper noun/capitalized, try Wikipedia
3. Cache both types of results separately
4. Show appropriate result in modal

### Pros:
✅ **Best of both worlds** - Definitions for common words, Wikipedia for proper nouns  
✅ **Smart fallback** - Automatically chooses best source  
✅ **Comprehensive coverage** - Handles both dictionary words and encyclopedic entries  
✅ **User-friendly** - Gets the right type of info for each word  

### Cons:
❌ **Two API calls** - More complex logic  
❌ **Network required** - Won't work offline  
❌ **Slower** - May need to wait for fallback if first fails  

### Implementation complexity: **Medium**
- Need to coordinate two APIs
- Logic to determine when to use which
- Caching strategy for both

---

## Approach 4: Embedded Dictionary (Offline-First)

### How it works:
- Pre-process and embed a dictionary database (like WordNet definitions)
- Store in compressed format similar to current word lists
- Lookup happens instantly, no API calls
- Optional: Fallback to online APIs if word not found

### Pros:
✅ **Offline-capable** - Works without internet  
✅ **Instant** - No network latency  
✅ **No rate limits** - Unlimited lookups  
✅ **Privacy** - No external API calls  
✅ **Consistent** - Same experience every time  

### Cons:
❌ **Large file size** - Dictionary data can be 10-50MB+  
❌ **Limited coverage** - Only words in embedded dictionary  
❌ **No Wikipedia** - Can't provide encyclopedic info  
❌ **Static** - Can't update without rebuilding file  

### Implementation complexity: **Medium-High**
- Need to extract and compress dictionary data
- Embed in HTML file (or load as separate JSON)
- Compression strategy to minimize size

---

## Approach 5: Client-Side NLP Library (compromise.js)

### How it works:
- Use `compromise.js` library (already considered earlier)
- Provides definitions, synonyms, and word info
- All client-side, no API calls
- Can combine with other approaches

### Pros:
✅ **Offline-capable** - Works without internet  
✅ **Fast** - Client-side processing  
✅ **Rich features** - Definitions, synonyms, related words  
✅ **No API keys** - Free to use  

### Cons:
❌ **Limited definitions** - Not as comprehensive as full dictionary  
❌ **Library size** - Adds ~200KB to file  
❌ **No Wikipedia** - Can't provide encyclopedic info  
❌ **May not cover all words** - Especially proper nouns, slang  

### Implementation complexity: **Low-Medium**
- Add library (CDN or embed)
- Use library's definition methods
- Combine with existing highlighting

---

## Approach 6: Progressive Enhancement (Cached + Online)

### How it works:
1. Start with embedded common word definitions (top 10k words)
2. On hover, check embedded cache first
3. If not found, try Dictionary API
4. If still not found, try Wikipedia for capitalized words
5. Cache all results in localStorage
6. Optionally preload definitions for visible words

### Pros:
✅ **Fast for common words** - Instant lookup from cache  
✅ **Comprehensive** - Falls back to APIs for rare words  
✅ **Offline-friendly** - Works for common words offline  
✅ **Smart caching** - Builds local dictionary over time  
✅ **Best UX** - Fast when possible, comprehensive when needed  

### Cons:
❌ **Complex** - Multiple data sources to manage  
❌ **Large initial file** - Embedded dictionary adds size  
❌ **Still needs network** - For rare words and Wikipedia  

### Implementation complexity: **High**
- Multiple data sources
- Caching strategy
- Preloading logic
- Fallback chain

---

## Recommended Approach: **Hybrid (Approach 3) with Caching**

### Why:
- **Best balance** of simplicity and functionality
- Dictionary API for common words (fast, accurate definitions)
- Wikipedia for proper nouns and concepts (comprehensive)
- localStorage caching prevents repeated API calls
- Works well for the use case (transcript analysis)

### Implementation Plan:
1. Add hover event listeners to all highlighted words
2. Show loading indicator in tooltip
3. Check localStorage cache first
4. If not cached:
   - Try Dictionary API first
   - If no result or word is capitalized, try Wikipedia
   - Cache result
5. Display in elegant modal/tooltip
6. Add debouncing to prevent too many API calls

### UI Considerations:
- **Tooltip/Modal design**: Clean, readable, positioned near cursor
- **Loading state**: Show spinner or "Loading..." text
- **Error handling**: "Definition not available" for failed lookups
- **Mobile-friendly**: Touch to show (since hover doesn't work on mobile)

---

## Alternative: Wikipedia-Only Approach

If simplicity is priority:
- Use only Wikipedia API
- Works for both dictionary words and proper nouns
- Single API to manage
- Good for transcripts (often contain names, places, concepts)

---

## Performance Considerations

### Caching Strategy:
- **localStorage**: Cache definitions indefinitely (or with expiry)
- **Session storage**: Cache for current session
- **Memory cache**: Keep recent lookups in JavaScript object

### Optimization:
- **Debouncing**: Wait 300ms before fetching (user might move cursor quickly)
- **Preloading**: Load definitions for visible words on page load
- **Batch requests**: If possible, fetch multiple words at once
- **Lazy loading**: Only fetch when user hovers (not on page load)

### Rate Limiting:
- Dictionary API: ~100 requests/minute (estimate)
- Wikipedia API: Generous limits, but should still cache
- Implement request queue if needed

---

## Mobile Considerations

Since hover doesn't work on mobile:
- **Tap to show**: Click/tap word to show definition
- **Long press**: Alternative interaction
- **Toggle mode**: Tap to enable "definition mode", then tap words

---

## Next Steps

1. **Choose approach** (recommended: Hybrid with caching)
2. **Design UI** - Tooltip/modal appearance
3. **Implement API integration** - Dictionary + Wikipedia
4. **Add caching layer** - localStorage
5. **Add mobile support** - Tap interactions
6. **Test performance** - Ensure smooth experience
7. **Polish UI** - Animations, positioning, styling

