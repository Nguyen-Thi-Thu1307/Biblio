(() => {
  const input = document.querySelector("#site-search");
  const form = input?.closest("form");
  const datalist = document.querySelector("#site-search-suggestions");
  if (!input || !form || !datalist) return;

  const storageKey = "biblio-search-history";
  const maxHistory = 8;
  let debounceTimer;
  let activeRequest;

  function readHistory() {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey) || "[]");
      return Array.isArray(saved)
        ? saved.filter((term) => typeof term === "string")
        : [];
    } catch {
      return [];
    }
  }

  function renderOptions(books = []) {
    const options = new Map();

    for (const term of readHistory()) {
      options.set(term.toLocaleLowerCase(), { value: term, label: "Tìm gần đây" });
    }

    for (const book of books) {
      if (book.title) {
        options.set(book.title.toLocaleLowerCase(), {
          value: book.title,
          label: `Sách · ${book.author || ""}`,
        });
      }
      if (book.author) {
        options.set(book.author.toLocaleLowerCase(), {
          value: book.author,
          label: "Tác giả",
        });
      }
    }

    datalist.replaceChildren(
      ...Array.from(options.values(), ({ value, label }) => {
        const option = document.createElement("option");
        option.value = value;
        option.label = label;
        return option;
      }),
    );
  }

  renderOptions();

  input.addEventListener("input", () => {
    window.clearTimeout(debounceTimer);
    activeRequest?.abort();
    renderOptions();

    const query = input.value.trim();
    if (!query) return;

    debounceTimer = window.setTimeout(async () => {
      activeRequest = new AbortController();
      try {
        const url = new URL(input.dataset.suggestionsUrl, window.location.origin);
        url.searchParams.set("q", query);
        const response = await fetch(url, { signal: activeRequest.signal });
        if (!response.ok) return;
        renderOptions(await response.json());
      } catch (error) {
        if (error.name !== "AbortError") renderOptions();
      }
    }, 180);
  });

  form.addEventListener("submit", () => {
    const term = input.value.trim();
    if (!term) return;

    const history = readHistory().filter(
      (savedTerm) => savedTerm.toLocaleLowerCase() !== term.toLocaleLowerCase(),
    );
    history.unshift(term);
    try {
      localStorage.setItem(storageKey, JSON.stringify(history.slice(0, maxHistory)));
    } catch {
      // Search remains usable when browser storage is unavailable.
    }
  });
})();