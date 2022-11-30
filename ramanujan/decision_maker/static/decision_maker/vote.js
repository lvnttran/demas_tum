function submitVote()
{
	var table = document.getElementById('valueTable');
	var data = '';
	for (let i = 1, row; row = table.rows[i]; i++)
	{
		for (let j = i + 1, cell = row.cells[j]; j++)
		{
			if (isNaN(cell.textContent))
			{
				alert("Illegal input. Please try again");
				return;
			}
			else
			{
				data += cell.textContent;
				data += ',';
			}
		}
	}

	document.getElementById('returndata').value = data;
	document.getElementById('dataform').submit();
}