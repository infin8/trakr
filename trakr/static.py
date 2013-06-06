dashboard = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title id='Description'>trakr Dashboard
    </title>
    <link rel="stylesheet" href="http://cdn.trakr.mobi/jqwidgets/styles/jqx.base.css" type="text/css" />
    <link rel="stylesheet" href="http://cdn.trakr.mobi/jqwidgets/styles/jqx.black.css" type="text/css" />
    <link rel="stylesheet" href="http://cdn.trakr.mobi/jqwidgets/styles/jqx.shinyblack.css" type="text/css" />
    <script type="text/javascript" src="http://cdn.trakr.mobi/scripts/jquery-1.8.3.min.js"></script>
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxcore.js"></script>
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxdata.js"></script> 
    
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxscrollbar.js"></script>
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxmenu.js"></script>
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxcheckbox.js"></script>
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxlistbox.js"></script>
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxdropdownlist.js"></script>
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxgrid.columnsresize.js"></script>
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxbuttons.js"></script>
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxgrid.js"></script>
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxgrid.sort.js"></script> 
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxgrid.pager.js"></script> 
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxgrid.selection.js"></script> 
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxgrid.edit.js"></script> 
    <script type="text/javascript" src="http://cdn.trakr.mobi/scripts/gettheme.js"></script>
    <script type="text/javascript">
        $(document).ready(function () {
            //var theme = getDemoTheme();
            var url = "%(url)s";
            // prepare the data
            var source =
            {
                datatype: "json",
                datafields: [
                    { name: 'id', type: 'string' },
                    { name: 'name', type: 'string' },
                    { name: 'clicks', type: 'int' },
                    { name: 'leads', type: 'int' },
                    { name: 'conversion', type: 'float' },
                    { name: 'payout', type: 'float' },
                    { name: 'revenue', type: 'float' },
                    { name: 'epc', type: 'float' },                    
                    { name: 'cpc', type: 'float' },
                    { name: 'spend', type: 'float' },
                    //{ name: 'discrepancy', type: 'float' },
                    { name: 'profit', type: 'float' }
                ],
                id: 'id',
                url: url
            };
            var dataAdapter = new $.jqx.dataAdapter(source);
            $("#jqxgrid").jqxGrid(
            {
                width: 960,
                source: dataAdapter,
                theme: 'black',
                pageable: true,
                sortable: true,
                //columnsresize: true,
                editable: true,
                ready: function(){
                    $("#jqxgrid").jqxGrid('setcolumnproperty', 'id', 'editable', false);
                    $("#jqxgrid").jqxGrid('setcolumnproperty', 'conversion', 'editable', false);
                    $("#jqxgrid").jqxGrid('setcolumnproperty', 'epc', 'editable', false); 
                    $("#jqxgrid").jqxGrid('setcolumnproperty', 'revenue', 'editable', false);
                    $("#jqxgrid").jqxGrid('setcolumnproperty', 'spend', 'editable', false); 
                    $("#jqxgrid").jqxGrid('setcolumnproperty', 'profit', 'editable', false);
                },
                columns: [
                  { text: 'ID', datafield: 'id', mindwidth: 50 },
                  { text: 'Name', datafield: 'name', minwidth: 150 },
                  { text: 'Clicks', datafield: 'clicks', width: 75 },
                  { text: 'Leads', datafield: 'leads', width: 75 },
                  { text: 'CR', datafield: 'conversion', width: 50, cellsformat: 'p1' },
                  { text: 'EPC', datafield: 'epc', width: 50, cellsformat: 'c3' },
                  { text: 'Revenue', datafield: 'revenue', width: 75, cellsformat: 'c2' },
                  { text: 'Payout', datafield: 'payout', width: 75, cellsformat: 'c2' },
                  { text: 'CPC', datafield: 'cpc', width: 50, cellsformat: 'c3' },
                  { text: 'Spend', datafield: 'spend', width: 75, cellsformat: 'c2' },
                  //{ text: 'Discrepancy', datafield: 'discrepancy', width: 50, cellsformat: 'p1' },
                  { text: 'Net Profit', datafield: 'profit', width: 100, cellsformat: 'c2' }
              ]
            });
            $("#jqxgrid").on('cellendedit', function (event) 
            {
                var column = args.datafield;
                var row = args.rowindex;var value = args.value;
                var oldvalue = args.oldvalue;
                if(column == 'payout'){
                    var leads = $('#jqxgrid').jqxGrid('getcellvalue', row, "leads");
                    var clicks = $('#jqxgrid').jqxGrid('getcellvalue', row, "clicks");
                    var revenue = $('#jqxgrid').jqxGrid('getcellvalue', row, "revenue");
                    var spend = $('#jqxgrid').jqxGrid('getcellvalue', row, "spend");
                    var revenue = value * leads
                    
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "revenue", revenue);
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "epc", revenue / clicks);
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "profit", revenue - spend);
                }
                if(column == 'cpc'){
                    var clicks = $('#jqxgrid').jqxGrid('getcellvalue', row, "clicks");
                    var discrepancy = $('#jqxgrid').jqxGrid('getcellvalue', row, "discrepancy") / 100;
                    var revenue = $('#jqxgrid').jqxGrid('getcellvalue', row, "revenue");
                    var spend = clicks * value; // * (1 + discrepancy)
                    
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "spend", spend);
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "profit", revenue - spend);
                }
                if(column == 'discrepancy'){
                    var clicks = $('#jqxgrid').jqxGrid('getcellvalue', row, "clicks");
                    var cpc = $('#jqxgrid').jqxGrid('getcellvalue', row, "cpc");
                    var revenue = $('#jqxgrid').jqxGrid('getcellvalue', row, "revenue");
                    var spend = clicks * cpc * (1 + value/100)
                    
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "spend", spend);
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "profit", revenue - spend);
                }
                if(column == 'leads'){
                    var clicks = $('#jqxgrid').jqxGrid('getcellvalue', row, "clicks");
                    var payout = $('#jqxgrid').jqxGrid('getcellvalue', row, "payout");
                    var spend = $('#jqxgrid').jqxGrid('getcellvalue', row, "spend");
                    var revenue = payout * value;
                    
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "conversion", value / clicks * 100);
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "epc", revenue / clicks);
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "revenue", revenue);
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "profit", revenue - spend);
                }
                if(column == 'clicks'){
                    var leads = $('#jqxgrid').jqxGrid('getcellvalue', row, "leads");
                    var payout = $('#jqxgrid').jqxGrid('getcellvalue', row, "payout");
                    var revenue = $('#jqxgrid').jqxGrid('getcellvalue', row, "revenue");
                    var cpc = $('#jqxgrid').jqxGrid('getcellvalue', row, "cpc");
                    var spend = cpc * value;
                    
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "conversion", leads / value * 100);
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "epc", revenue / value);
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "spend", spend);
                    $("#jqxgrid").jqxGrid('setcellvalue', row, "profit", revenue - spend);
                }
            });
        });
    </script>
</head>
<body class='default'>
    <div id='jqxWidget' style="font-size: 13px; font-family: Verdana; float: left;">
        <div id="jqxgrid">
        </div>
     </div>
</body>
</html>
"""

trackingjs = """
var query = window.location.search.replace('?', '&');
var referer = escape(document.referrer);
var metas = document.getElementsByName('lpid');
var lpid = '';
if(metas.length > 0){lpid = metas[0].content;}
document.write('<scr'+'ipt language="JavaScript" src="%(lp)s?referer='+referer+'&lpid='+lpid+query+'" type="text/javascript"></scr' + 'ipt>');
a = document.links;
for (var i= 0; i < a.length; ++i){
    a[i].onclick = clickListener;
}
function clickListener(e) 
{   
    var clickedElement=(window.event)
                        ? window.event.srcElement
                        : e.target,
        tags=document.getElementsByTagName(clickedElement.tagName);
    if(clickedElement.href){
        document.write('<scr'+'ipt language="JavaScript" src="%(ct)s?url='+escape(clickedElement.href)+'&cid='+cid+'" type="text/javascript"></scr' + 'ipt>');
        return false;
    }
}
"""