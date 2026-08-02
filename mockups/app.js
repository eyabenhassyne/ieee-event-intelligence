window.MockupApp = {
  renderPage(navHtml) {
    const nav = document.querySelector("[data-nav]");
    if (nav && typeof navHtml === "string" && navHtml.trim()) {
      nav.innerHTML = navHtml;
    }
  },
};
