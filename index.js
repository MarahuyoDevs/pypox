const fs = require("fs");

// Specify the file path
const filePath = "./CHANGELOG.md";

// Read the file contents
fs.readFile(filePath, "utf8", (err, data) => {
  if (err) {
    console.error(err);
    return;
  }

  // Store the changelog entries as an object
  const changelog = {};

  // Split the data by new lines
  const lines = data.split("\n");

  // Iterate through each line
  let currentVersion = "";
  lines.forEach((line) => {
    // Check if the line is a version heading
    if (line.startsWith("## ")) {
      // Remove the '## ' characters and trim any leading/trailing spaces
      currentVersion = line.replace("## ", "").trim();
      if (currentVersion !== "") {
        changelog[currentVersion] = "";
      }
    } else {
      // Append the line to the current version's description
      if (currentVersion !== "") {
        changelog[currentVersion] += line + "\n";
      }
    }
  });

  // Use the changelog object as needed
  console.log(Object.keys(changelog)[0]);
});
