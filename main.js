// main.js
// This script finds the latest output folder and lists the CSV files inside it as buttons.
// When a button is clicked, it fetches and renders the CSV as a table using PapaParse and DataTables.

$(document).ready(function () {
  // Hardcoded for demo: in a real app, this would be fetched from the server
  // List of output folders (should be sorted by timestamp descending)
  const outputFolders = ["2025-05-22_00h17", "2025-05-22_00h10"];
  // Pick the latest
  const latestFolder = outputFolders[0];
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
    const fileUrl = `output/${latestFolder}/${file}`;
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
            // Build HTML table
            let html =
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
            $("#csv-table").DataTable({
              pageLength: -1,
              lengthMenu: [[-1], ["All"]],
              scrollX: true,
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
