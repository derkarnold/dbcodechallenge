// My code.
function SQLEngine(database) {
    // Assuming token boundaries are whitespace.
    var TOKEN_BOUNDARY = "\\s*";

    // The token for the boundary between columns in the
    // select clause.
    var COLUMN_SEPARATOR = `,${TOKEN_BOUNDARY}`;
    var COLUMN_SEPARATOR_REGEXP = RegExp(COLUMN_SEPARATOR);

    // Regular expression to tokenise our query.
    var QUERY_REGEXP = new RegExp([
        "select",
        `(?<columns>(?:[a-z.]+)(?:${COLUMN_SEPARATOR}[a-z.]+)*?)`,
        "from",
        "(?<table>[a-z]+)",
        "(?:where",
        "(?<whereColumn>[a-z.]+)",
        "(?<whereOp><>|[<>=])",
        "(?<whereValue>(?:'[^']+')|(?:\"[^\"]+\")|(?:[0-9]+))" +
        ")?",
    ].join(TOKEN_BOUNDARY), "i");

    this.execute = function (query) {
        var match = query.match(QUERY_REGEXP);
        if (!match) {
            throw `Invalid query: ${query}`;
        }
        var groups = match.groups;
        var tableName = groups["table"];

        var columns = groups["columns"].split(COLUMN_SEPARATOR_REGEXP);
        var selectColumns = columns
            .map((c) => this.processAndCheckColumnQuery(c, tableName));

        var whereFilter = this.createWhereFilter(
            groups["whereColumn"],
            groups["whereOp"],
            groups["whereValue"],
            tableName,
        );

        var records = database[tableName];
        var results = [];
        for (var i = 0; i < records.length; ++i) {
            var record = records[i];
            if (whereFilter(record)) {
                var result = Object();
                for (var c = 0; c < columns.length; ++c) {
                    result[columns[c]] = record[selectColumns[c]];
                }
                results.push(result);
            }
        }

        return results;
    }

    this.processAndCheckColumnQuery = function (column, tableName) {
        var [columnTableName, columnName] = column.split(".");
        if (columnTableName != tableName) {
            throw `Unknown table name in query: ${columnTableName}`;
        }
        return columnName;
    }

    this.createWhereFilter = function (column, op, value, tableName) {
        if (!column && !op && !value) {
            return (record) => true;
        } else {
            var pColumnName
                = this.processAndCheckColumnQuery(column, tableName);
            var pValue = this.processWhereValue(value);
            switch (op) {
                case "=":
                    return (record) => record[pColumnName] == pValue;
                case "<":
                    return (record) => record[pColumnName] < pValue;
                case ">":
                    return (record) => record[pColumnName] > pValue;
                case "<>":
                    return (record) => record[pColumnName] != pValue;
                default:
                    throw `Invalid op: ${op}`;
            }
        }
    }

    this.processWhereValue = function (value) {
        if (value[0] == "'" || value[0] == '"') {
            // String.
            return value.slice(1, value.length - 1);
        } else {
            // Integer.
            return parseInt(value);
        }
    }
}


// Code to test my code against:
var dummyDatabase = {
    employees: [{
        id: 1,
        name: 'Alice',
        phone: '12345678',
    },
    {
        id: 2,
        name: 'Bob',
        phone: '87654321',
    }
    ],
};

describe('execution', function () {
    var engine = new SQLEngine(dummyDatabase);

    it('should SELECT columns', function () {
        var actual = engine.execute('SELECT employees.name FROM employees');
        expect(actual).to.deep.equal(
            [{
                "employees.name": "Alice"
            }, {
                "employees.name": "Bob"
            }]);
    });

    it('should apply WHERE', function () {
        var actual = engine.execute('SELECT employees.id, employees.name FROM employees WHERE employees.id = 1');
        expect(actual).to.deep.equal([{
            "employees.id": 1,
            "employees.name": "Alice"
        }]);
    });
});
