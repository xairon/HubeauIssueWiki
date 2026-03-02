(function() {
    'use strict';

    var searchIndex = [];
    var debounceTimer = null;
    var input = document.getElementById('searchInput');
    var resultsContainer = document.getElementById('searchResults');

    // Load search index
    fetch('search-index.json')
        .then(function(r) { return r.json(); })
        .then(function(data) { searchIndex = data; })
        .catch(function() { console.warn('Could not load search index.'); });

    // Debounced search
    input.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        var val = this.value.trim();
        debounceTimer = setTimeout(function() { performSearch(val); }, 200);
    });

    // Close results on click outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-container')) {
            resultsContainer.classList.remove('visible');
        }
    });

    // Re-open on focus if there is a query
    input.addEventListener('focus', function() {
        if (this.value.trim().length > 0 && resultsContainer.children.length > 0) {
            resultsContainer.classList.add('visible');
        }
    });

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.textContent;
    }

    function performSearch(query) {
        // Clear previous results
        while (resultsContainer.firstChild) {
            resultsContainer.removeChild(resultsContainer.firstChild);
        }

        if (query.length < 2) {
            resultsContainer.classList.remove('visible');
            return;
        }

        var lowerQ = query.toLowerCase();
        var matches = searchIndex.filter(function(entry) {
            return entry.text.toLowerCase().indexOf(lowerQ) !== -1 ||
                   entry.title.toLowerCase().indexOf(lowerQ) !== -1 ||
                   entry.section.toLowerCase().indexOf(lowerQ) !== -1;
        }).slice(0, 20);

        if (matches.length === 0) {
            var noRes = document.createElement('div');
            noRes.className = 'search-no-results';
            noRes.textContent = 'Aucun r\u00e9sultat trouv\u00e9';
            resultsContainer.appendChild(noRes);
            resultsContainer.classList.add('visible');
            return;
        }

        matches.forEach(function(entry) {
            var item = document.createElement('a');
            item.className = 'search-result-item';
            item.href = entry.url;

            // Tags row
            var tagsDiv = document.createElement('div');
            tagsDiv.className = 'search-result-tags';

            var apiTag = document.createElement('span');
            apiTag.className = 'search-tag search-tag-api';
            apiTag.textContent = entry.api;
            tagsDiv.appendChild(apiTag);

            var secTag = document.createElement('span');
            secTag.className = 'search-tag search-tag-section';
            secTag.textContent = entry.section;
            tagsDiv.appendChild(secTag);

            item.appendChild(tagsDiv);

            // Text with highlighting via DOM
            var displayText = entry.text;
            if (displayText.length > 160) {
                var idx = displayText.toLowerCase().indexOf(lowerQ);
                if (idx > 60) {
                    displayText = '...' + displayText.substring(idx - 40);
                }
                if (displayText.length > 160) {
                    displayText = displayText.substring(0, 157) + '...';
                }
            }

            var textDiv = document.createElement('div');
            textDiv.className = 'search-result-text';

            // Split on query matches and build text nodes + mark elements
            var escapedQ = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            var regex = new RegExp('(' + escapedQ + ')', 'gi');
            var parts = displayText.split(regex);
            parts.forEach(function(part) {
                if (part.toLowerCase() === query.toLowerCase()) {
                    var mark = document.createElement('mark');
                    mark.textContent = part;
                    textDiv.appendChild(mark);
                } else {
                    textDiv.appendChild(document.createTextNode(part));
                }
            });

            item.appendChild(textDiv);
            resultsContainer.appendChild(item);
        });

        resultsContainer.classList.add('visible');
    }
})();
