document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("search-id");
  const searchBtn = document.getElementById("search-btn");
  const resultsContainer = document.getElementById("results");
  const resultInfo = document.getElementById("result-info");
  const paginationContainer = document.getElementById("pagination");

  let currentPage = 1;
  let isSearching = false;
  let currentQuery = "";

  // Load all documents on page load
  loadAllDocuments(1);

  function loadAllDocuments(page) {
    isSearching = false;
    currentPage = page;

    fetch(`/get-all-docs?page=${page}`)
      .then((response) => response.json())
      .then((data) => {
        displayResults(data, false);
      })
      .catch((error) => console.error("Error:", error));
  }

  function performSearch() {
    const query = searchInput.value.trim();
    if (!query) {
      loadAllDocuments(1);
      return;
    }

    isSearching = true;
    currentQuery = query;
    currentPage = 1;

    fetch(`/search?q=${encodeURIComponent(query)}&page=1`)
      .then((response) => response.json())
      .then((data) => {
        displayResults(data, true);
      })
      .catch((error) => console.error("Error:", error));
  }

  function displayResults(data, isSearch) {
    const { query, total, total_pages, page, results } = data;

    if (isSearch) {
      resultInfo.innerHTML = `<p>Hasil untuk "${query}" (${total} hasil)</p>`;
    } else {
      resultInfo.innerHTML = `<p>Semua Komentar (${total} total)</p>`;
    }

    if (results.length === 0) {
      resultsContainer.innerHTML = '<p style="text-align: center; padding: 40px; font-size: 16px;">Tidak ada hasil ditemukan</p>';
      paginationContainer.innerHTML = "";
      return;
    }

    resultsContainer.innerHTML = results
      .map((doc) => {
        let infoContent = "—";
        if (isSearch && doc.score) {
          infoContent = `Similarity: ${doc.score}`;
        }
        return `
        <div class="container">
          <div class="content">
            <p>${doc.full_text}</p>
          </div>
          <div class="info">${infoContent}</div>
        </div>
      `;
      })
      .join("");

    // Display pagination
    if (total_pages > 1) {
      displayPagination(page, total_pages, isSearch);
    } else {
      paginationContainer.innerHTML = "";
    }
  }

  function displayPagination(currentPageNum, totalPages, isSearch) {
    let paginationHTML = '<div class="pagination">';

    // Previous button
    if (currentPageNum > 1) {
      paginationHTML += `<button onclick="previousPage(${isSearch})">← Sebelumnya</button>`;
    } else {
      paginationHTML += `<button disabled>← Sebelumnya</button>`;
    }

    // Page numbers
    paginationHTML += `<span> Halaman ${currentPageNum} dari ${totalPages} </span>`;

    // Next button
    if (currentPageNum < totalPages) {
      paginationHTML += `<button onclick="nextPage(${isSearch})">Berikutnya →</button>`;
    } else {
      paginationHTML += `<button disabled>Berikutnya →</button>`;
    }

    paginationHTML += "</div>";
    paginationContainer.innerHTML = paginationHTML;
  }

  window.previousPage = function (isSearch) {
    if (currentPage > 1) {
      currentPage--;
      if (isSearch) {
        fetch(`/search?q=${encodeURIComponent(currentQuery)}&page=${currentPage}`)
          .then((response) => response.json())
          .then((data) => displayResults(data, true))
          .catch((error) => console.error("Error:", error));
      } else {
        loadAllDocuments(currentPage);
      }
    }
  };

  window.nextPage = function (isSearch) {
    currentPage++;
    if (isSearch) {
      fetch(`/search?q=${encodeURIComponent(currentQuery)}&page=${currentPage}`)
        .then((response) => response.json())
        .then((data) => displayResults(data, true))
        .catch((error) => console.error("Error:", error));
    } else {
      loadAllDocuments(currentPage);
    }
  };

  searchBtn.addEventListener("click", performSearch);
  searchInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") performSearch();
  });
});
