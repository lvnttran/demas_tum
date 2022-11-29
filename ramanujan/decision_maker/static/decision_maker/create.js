function addTable() 
{   
    var candidates = document.getElementById("candidates").value.split(',');
    var criterias = document.getElementById("criterias").value.split(',');
    var form = document.getElementById("dataform");      

    var table = document.createElement('table');
    table.id = "scoretable"
    table.name = "scores"
    table.border='1';    
    var tableBody = document.createElement('tbody');
    table.appendChild(tableBody);
    
    var tr = document.createElement('tr');
    tableBody.appendChild(tr)
    var td = document.createElement('td');
    td.width = '80'
    td.appendChild(document.createTextNode(" "));
    tr.appendChild(td);
    for (let i of candidates)
    {
        td = document.createElement('td');
        td.width='80';
        td.appendChild(document.createTextNode(i));
        tr.appendChild(td);
    }

    for (let i of criterias)
    {
        tr = document.createElement('tr');
        tableBody.appendChild(tr);
        td = document.createElement('td');
        td.width='80';
        td.appendChild(document.createTextNode(i));
        tr.appendChild(td);

       for (var j=0; j < candidates.length; j++)
       {
           td = document.createElement('td');
           td.width='80';
           td.contentEditable = 'True';
           td.appendChild(document.createTextNode("0"));
           tr.appendChild(td);
       }
    }

    form.appendChild(table);    
    document.getElementById("submitbtn").onclick = submitTable;
}


function submitTable()
{
    if (checkTable() == false)
    {
        alert("Illegal input. Please try again")
    }
    else
    {        
        document.getElementById('dataform').submit();
    }
}


function checkTable()
{
    var table = document.getElementById("scoretable");
    var data = document.getElementById('question').value + ',\n';

    var row = table.rows[0];
    var cell;

    for (let j = 1; cell = row.cells[j]; j++)
    {
        data += cell.textContent;
        data += ','
    }
    data += '\n';

    for (let i = 1; row = table.rows[i]; i++)
    {
        data += row.cells[0].textContent;
        data += ','
    }
    data += '\n';

    for (let i = 1; row = table.rows[i]; i++)
    {
        for (let j = 1; cell = row.cells[j]; j++)
        {
            if (isNaN(cell.textContent))
            {
                return false;
            }
            else
            {
                data += cell.textContent;
                data += ','
            }
        }
    }

    document.getElementById('returndata').value = data;
    return true;
}