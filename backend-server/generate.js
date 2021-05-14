'use strict';
const fs = require('fs');
function main() {
    // Get all handlers
    var results = getAllFilesFromFolder('handlers');
    var output = "'use strict';\n";
    results.forEach(file => {
        output += "require('../" + file + "');\n";
    });
    fs.writeFileSync('tests/allTests-spec.js', output);
}

/**
 * Credit to Samuel Ondrek
 * http://stackoverflow.com/questions/20822273/best-way-to-get-folder-and-file-list-in-javascript
 * Gets all files given a path to a folder
 * @param {String} dir - The path to the folder
 * @returns {Array} All of the files contained within the directory and subdirectories
 **/
function getAllFilesFromFolder(dir) {
    var results = [];
    fs.readdirSync(dir).forEach(function(fileInDir) {
        var file = dir + '/' + fileInDir;
        var stat = fs.statSync(file);
        if (stat && stat.isDirectory()) {
            results = results.concat(getAllFilesFromFolder(file));
        } else results.push(file);
    });
    return results;
}

main();
