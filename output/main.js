// main.js
// This script finds the latest output folder and lists the CSV files inside it as buttons.
// When a button is clicked, it fetches and renders the CSV as a table using PapaParse and DataTables.

$(document).ready(function () {
  // List of CSV files in the latest folder (should be fetched from server in real app)
  const csvFiles = ["Batting.csv", "Pitching.csv", "Fielding.csv"];

  // Render buttons for each CSV file
  const $buttons = $("#csv-buttons");
  csvFiles.forEach(function (file, idx) {
    const btn = $(
      `<button class="btn btn-primary me-2 mb-2" data-file="${file}">${file.replace(
        ".csv",
        ""
      )}</button>`
    );
    btn.on("click", function () {
      renderCsvTable(file);
      // Highlight active button
      $buttons
        .find("button")
        .removeClass("btn-success")
        .addClass("btn-primary");
      $(this).removeClass("btn-primary").addClass("btn-success");
    });
    $buttons.append(btn);
    // Auto-load the first CSV
    if (idx === 0) btn.trigger("click");
  });

  function renderCsvTable(file) {
    const fileUrl = `${file}`;
    $("#table-container").html('<div class="text-muted">Loading...</div>');
    $.ajax({
      url: fileUrl,
      dataType: "text",
      success: function (csv) {
        Papa.parse(csv, {
          header: true,
          skipEmptyLines: true,
          complete: function (results) {
            const data = results.data;
            const columns = results.meta.fields;
            // Build filter dropdowns if columns exist
            let filterHtml = "";
            if (columns.includes("Round") || columns.includes("Team")) {
              filterHtml +=
                '<div id="custom-filters" class="d-flex flex-column align-items-start mb-3">';
              if (columns.includes("Round")) {
                const rounds = Array.from(
                  new Set(data.map((row) => row["Round"]).filter(Boolean))
                ).sort();
                filterHtml +=
                  '<div class="mb-2"><label class="mb-1">Round:</label><div id="round-checkboxes">';
                rounds.forEach((round) => {
                  filterHtml += `<div class=\"form-check form-check-inline me-3\"><input class=\"form-check-input\" type=\"checkbox\" name=\"filter-round\" value=\"${round}\" id=\"filter-round-${round}\"><label class=\"form-check-label\" for=\"filter-round-${round}\">${round}</label></div>`;
                });
                filterHtml += "</div></div>";
              }
              if (columns.includes("Team")) {
                const teams = Array.from(
                  new Set(data.map((row) => row["Team"]).filter(Boolean))
                ).sort();
                filterHtml +=
                  '<div class="mb-2"><label class="mb-1">Team:</label><select id="filter-team" class="form-select form-select-sm w-auto ms-2"><option value="">All</option>';
                teams.forEach((team) => {
                  filterHtml += `<option value=\"${team}\">${team}</option>`;
                });
                filterHtml += "</select></div>";
              }
              // Search input
              filterHtml +=
                '<div class="mb-2"><label class="mb-1">Search:</label><input type="search" id="custom-search" class="form-control form-control-sm w-auto ms-2" placeholder="Search"></div>';
              filterHtml += "</div>";
            }
            // Build HTML table
            let html =
              filterHtml +
              '<div class="table-responsive"><table id="csv-table" class="display table table-striped table-bordered" style="width:100%"><thead><tr>';
            // Find the index of the 'Name' column
            const nameColIdx = columns.findIndex(
              (col) => col.trim().toLowerCase() === "name"
            );
            columns.forEach((col, idx) => {
              if (idx === nameColIdx) {
                html += `<th class="sticky-name-col">${col}</th>`;
              } else {
                html += `<th>${col}</th>`;
              }
            });
            html += "</tr></thead><tbody>";
            data.forEach((row) => {
              html += "<tr>";
              columns.forEach((col, idx) => {
                if (idx === nameColIdx) {
                  html += `<td class="sticky-name-col">${row[col] || ""}</td>`;
                } else {
                  html += `<td>${row[col] || ""}</td>`;
                }
              });
              html += "</tr>";
            });
            html += "</tbody></table></div>";
            // Export button container
            html +=
              '<div class="d-flex justify-content-center mt-3 mb-5"><button id="export-csv-btn" class="btn btn-outline-secondary">Export CSV</button></div>';
            $("#table-container").html(html);
            // Activate DataTables
            const table = $("#csv-table").DataTable({
              pageLength: -1,
              lengthMenu: [[-1], ["All"]],
              scrollX: true,
              dom: "tip",
              fixedHeader: true,
            });
            // Export CSV logic
            $("#export-csv-btn")
              .off("click")
              .on("click", function () {
                // Get filtered data
                const filteredData = table
                  .rows({ search: "applied" })
                  .data()
                  .toArray();
                // Convert to array of objects
                const exportData = filteredData.map((rowArr) => {
                  const obj = {};
                  columns.forEach((col, idx) => {
                    obj[col] = rowArr[idx];
                  });
                  return obj;
                });
                // Build dynamic filename based on filters
                let base = file.replace(/\.csv$/, "");
                let parts = [];
                // Round filter
                const roundChecked = $("input[name='filter-round']:checked")
                  .map(function () {
                    return $(this).val();
                  })
                  .get();
                if (roundChecked.length > 0) {
                  parts.push(
                    "Round-" +
                      roundChecked
                        .map((v) => v.replace(/[^\w-]/g, ""))
                        .join("-")
                  );
                }
                // Team filter
                const teamVal = $("#filter-team").val();
                if (teamVal) {
                  parts.push("Team-" + teamVal.replace(/[^\w-]/g, ""));
                }
                // Search filter
                const searchVal = $("#custom-search").val();
                if (searchVal) {
                  parts.push("Search-" + searchVal.replace(/[^\w-]/g, ""));
                }
                let filename = base;
                if (parts.length > 0) {
                  filename += "_" + parts.join("_");
                } else {
                  filename += "_filtered";
                }
                filename += ".csv";
                // Use PapaParse to unparse to CSV
                const csv = Papa.unparse(exportData, { columns });
                // Use FileSaver.js to save
                const blob = new Blob([csv], {
                  type: "text/csv;charset=utf-8;",
                });
                saveAs(blob, filename);
              });
            // Filtering logic
            if (columns.includes("Round")) {
              $(document)
                .off("change", "input[name='filter-round']")
                .on("change", "input[name='filter-round']", function () {
                  const checked = $("input[name='filter-round']:checked")
                    .map(function () {
                      return $(this).val();
                    })
                    .get();
                  if (checked.length === 0) {
                    table
                      .column(columns.indexOf("Round"))
                      .search("", true, false)
                      .draw();
                  } else {
                    // Build regex for OR search
                    const regex = checked
                      .map((val) => `^${$.escapeSelector(val)}$`)
                      .join("|");
                    table
                      .column(columns.indexOf("Round"))
                      .search(regex, true, false)
                      .draw();
                  }
                });
            }
            if (columns.includes("Team")) {
              $("#filter-team").on("change", function () {
                const val = $(this).val();
                table
                  .column(columns.indexOf("Team"))
                  .search(
                    val ? "^" + $.escapeSelector(val) + "$" : "",
                    true,
                    false
                  )
                  .draw();
              });
            }
            // Sticky header on scroll
            $(window)
              .off("scroll.stickyHeader")
              .on("scroll.stickyHeader", function () {
                var $table = $("#csv-table");
                if ($table.length === 0) return;
                var $thead = $table.find("thead");
                var offset = $table.offset().top;
                var scrollTop = $(window).scrollTop();

                if (scrollTop > offset) {
                  if (!$thead.hasClass("sticky-header")) {
                    $thead.addClass("sticky-header");
                    // Add a placeholder row to prevent layout shift
                    if (
                      $thead.find(".sticky-header-placeholder").length === 0
                    ) {
                      var $placeholder = $thead
                        .find("tr")
                        .first()
                        .clone()
                        .addClass("sticky-header-placeholder");
                      $thead.append($placeholder);
                    }
                  }
                } else {
                  $thead.removeClass("sticky-header");
                  $thead.find(".sticky-header-placeholder").remove();
                }
              });
            // Custom search input logic
            $("#custom-search").on("input", function () {
              table.search($(this).val()).draw();
            });
          },
          error: function () {
            $("#table-container").html(
              '<div class="text-danger">Failed to parse CSV.</div>'
            );
          },
        });
      },
      error: function () {
        $("#table-container").html(
          '<div class="text-danger">Failed to load CSV file.</div>'
        );
      },
    });
  }
});
