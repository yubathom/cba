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
              filterHtml += '<div class="row mb-3">';
              if (columns.includes("Round")) {
                const rounds = Array.from(
                  new Set(data.map((row) => row["Round"]).filter(Boolean))
                ).sort();
                filterHtml +=
                  '<div class="col-auto"><label class="me-2">Round:</label><select id="filter-round" class="form-select form-select-sm"><option value="">All</option>';
                rounds.forEach((round) => {
                  filterHtml += `<option value="${round}">${round}</option>`;
                });
                filterHtml += "</select></div>";
              }
              if (columns.includes("Team")) {
                const teams = Array.from(
                  new Set(data.map((row) => row["Team"]).filter(Boolean))
                ).sort();
                filterHtml +=
                  '<div class="col-auto"><label class="me-2">Team:</label><select id="filter-team" class="form-select form-select-sm"><option value="">All</option>';
                teams.forEach((team) => {
                  filterHtml += `<option value="${team}">${team}</option>`;
                });
                filterHtml += "</select></div>";
              }
              filterHtml += "</div>";
            }
            // Build HTML table
            let html =
              filterHtml +
              '<table id="csv-table" class="display table table-striped table-bordered" style="width:100%"><thead><tr>';
            columns.forEach((col) => (html += `<th>${col}</th>`));
            html += "</tr></thead><tbody>";
            data.forEach((row) => {
              html += "<tr>";
              columns.forEach((col) => (html += `<td>${row[col] || ""}</td>`));
              html += "</tr>";
            });
            html += "</tbody></table>";
            $("#table-container").html(html);
            // Activate DataTables
            const table = $("#csv-table").DataTable({
              pageLength: -1,
              lengthMenu: [[-1], ["All"]],
              scrollX: true,
              dom: "ftip",
              fixedHeader: true,
            });
            // Filtering logic
            if (columns.includes("Round")) {
              $("#filter-round").on("change", function () {
                const val = $(this).val();
                table
                  .column(columns.indexOf("Round"))
                  .search(
                    val ? "^" + $.escapeSelector(val) + "$" : "",
                    true,
                    false
                  )
                  .draw();
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
