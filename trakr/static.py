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
    <!--<script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxgrid.columnsresize.js"></script>-->
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxbuttons.js"></script>
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxgrid.js"></script>
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxgrid.sort.js"></script> 
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxgrid.pager.js"></script> 
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxgrid.selection.js"></script> 
    <script type="text/javascript" src="http://cdn.trakr.mobi/jqwidgets/jqxgrid.edit.js"></script> 
    <script type="text/javascript" src="http://cdn.trakr.mobi/scripts/gettheme.js"></script>
    <script type="text/javascript">
        function save_campaign(id, name, payout, cpc, error){
            $.post('/save_campaign', {
                id: id,
                name: name,
                payout: payout,
                cpc: cpc,
                error: error / 100
            });
        }
        function update(row, column, value){
                    if(column == 'name'){
                        var cpc = $('#jqxgrid').jqxGrid('getcellvalue', row, "cpc");
                        var error = $('#jqxgrid').jqxGrid('getcellvalue', row, "error");
                        var payout = $('#jqxgrid').jqxGrid('getcellvalue', row, "payout");
                        var id = $('#jqxgrid').jqxGrid('getcellvalue', row, "id");
                        save_campaign(id, value, payout, cpc, error)
                        
                    }
                    if(column == 'payout'){
                        var leads = $('#jqxgrid').jqxGrid('getcellvalue', row, "leads");
                        var clicks = $('#jqxgrid').jqxGrid('getcellvalue', row, "clicks");
                        var revenue = $('#jqxgrid').jqxGrid('getcellvalue', row, "revenue");
                        var spend = $('#jqxgrid').jqxGrid('getcellvalue', row, "spend");
                        var revenue = value * leads
                        
                        $("#jqxgrid").jqxGrid('setcellvalue', row, "revenue", revenue);
                        $("#jqxgrid").jqxGrid('setcellvalue', row, "epc", revenue / clicks);
                        $("#jqxgrid").jqxGrid('setcellvalue', row, "profit", revenue - spend);

                        var name = $('#jqxgrid').jqxGrid('getcellvalue', row, "name");
                        var cpc = $('#jqxgrid').jqxGrid('getcellvalue', row, "cpc");
                        var error = $('#jqxgrid').jqxGrid('getcellvalue', row, "error");
                        var id = $('#jqxgrid').jqxGrid('getcellvalue', row, "id");
                        save_campaign(id, name, value, cpc, error)
                    }
                    if(column == 'cpc'){
                        var clicks = $('#jqxgrid').jqxGrid('getcellvalue', row, "clicks");
                        var error = $('#jqxgrid').jqxGrid('getcellvalue', row, "error") / 100;
                        var revenue = $('#jqxgrid').jqxGrid('getcellvalue', row, "revenue");
                        var spend = clicks * value; // * (1 + error)
                        
                        $("#jqxgrid").jqxGrid('setcellvalue', row, "spend", spend);
                        $("#jqxgrid").jqxGrid('setcellvalue', row, "profit", revenue - spend);
                        
                        var payout = $('#jqxgrid').jqxGrid('getcellvalue', row, "payout");
                        var name = $('#jqxgrid').jqxGrid('getcellvalue', row, "name");
                        var error = $('#jqxgrid').jqxGrid('getcellvalue', row, "error");
                        var id = $('#jqxgrid').jqxGrid('getcellvalue', row, "id");
                        save_campaign(id, name, payout, value, error);
                    }
                    if(column == 'error'){
                        var error = $('#jqxgrid').jqxGrid('getcellvalue', row, "error");
                        if(value == error){return false;}
                        var clicks = Math.round((1 + value/100) * $('#jqxgrid').jqxGrid('getcellvalue', row, "clicks"));
                        var cpc = $('#jqxgrid').jqxGrid('getcellvalue', row, "cpc");
                        var revenue = $('#jqxgrid').jqxGrid('getcellvalue', row, "revenue");
                        var spend = clicks * cpc
                        
                        $("#jqxgrid").jqxGrid('setcellvalue', row, "clicks", clicks);
                        $("#jqxgrid").jqxGrid('setcellvalue', row, "spend", spend);
                        $("#jqxgrid").jqxGrid('setcellvalue', row, "profit", revenue - spend);
                        $("#jqxgrid").jqxGrid('setcellvalue', row, "clicks", clicks);
                        update(row, 'clicks', clicks);
                        
                        var payout = $('#jqxgrid').jqxGrid('getcellvalue', row, "payout");
                        var name = $('#jqxgrid').jqxGrid('getcellvalue', row, "name");
                        var id = $('#jqxgrid').jqxGrid('getcellvalue', row, "id");
                        save_campaign(id, name, payout, cpc, value);
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
                }
        $(document).ready(function () {
            var theme = 'black';
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
                    { name: 'error', type: 'float' },
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
                theme: theme,
                pageable: true,
                sortable: true,
                //columnsresize: true,
                virtualmode: true,
                editable: true,
                rendergridrows: function(params){
                    var rows = params.data;
                    var data = {};
                    for (var i = 0; i < rows.length; i++) {
                        row = rows[i];
                        
                        row.clicks = row.clicks * (1 + row.error);
                        row.conversion = row.leads / row.clicks;
                        row.revenue = row.leads * row.payout;
                        row.spend = row.clicks * row.cpc;
                        row.profit = row.revenue - row.spend;
                        row.epc = row.revenue / row.clicks;
                        row.error = row.error * 100;
                        
                        data[i] = row;
                    }
                    
                    return data;
                },
                ready: function(){
                    $("#jqxgrid").jqxGrid('setcolumnproperty', 'id', 'editable', false);
                    $("#jqxgrid").jqxGrid('setcolumnproperty', 'conversion', 'editable', false);
                    $("#jqxgrid").jqxGrid('setcolumnproperty', 'epc', 'editable', false); 
                    $("#jqxgrid").jqxGrid('setcolumnproperty', 'revenue', 'editable', false);
                    $("#jqxgrid").jqxGrid('setcolumnproperty', 'spend', 'editable', false); 
                    $("#jqxgrid").jqxGrid('setcolumnproperty', 'profit', 'editable', false);
                },
                columns: [
                  { text: 'ID', datafield: 'id', mindwidth: 50, }, /**cellsrenderer: function (row, column, value) {
                        var button = $("<u/>",{
                            id: 'id',
                            //value: value,
                            //type: 'button',
                        }).html(value);
                        
                        button.jqxButton({ theme: theme });
                        button.click(function(){});
                        
                        return $("<p>").append(button).html();
                    }},**/
                  { text: 'Name', datafield: 'name', minwidth: 150 },
                  { text: 'Clicks', datafield: 'clicks', width: 75, cellsformat: 'n' },
                  { text: 'Leads', datafield: 'leads', width: 75, cellsformat: 'n' },
                  { text: 'CR', datafield: 'conversion', width: 50, cellsformat: 'p1' },
                  { text: 'EPC', datafield: 'epc', width: 50, cellsformat: 'c3' },
                  { text: 'Revenue', datafield: 'revenue', width: 75, cellsformat: 'c2' },
                  { text: 'Payout', datafield: 'payout', width: 75, cellsformat: 'c2' },
                  { text: 'CPC', datafield: 'cpc', width: 50, cellsformat: 'c3' },
                  { text: 'Spend', datafield: 'spend', width: 75, cellsformat: 'c2' },
                  { text: 'Error', datafield: 'error', width: 50, cellsformat: 'p1' },
                  { text: 'Net Profit', datafield: 'profit', width: 100, cellsformat: 'c2' }
              ]
            });
            $("#jqxgrid").on('cellendedit', function (event) 
            {
                var column = args.datafield;
                var row = args.rowindex;var value = args.value;
                var oldvalue = args.oldvalue;
                
                update(row, column, value);
            });
            $("#refresh").jqxButton({ theme: theme });
            $("#refresh").click(function () {
                $("#jqxgrid").jqxGrid('updatebounddata');
            });
        });
    </script>
</head>
<body class='default'>
    <div id='jqxWidget' style="font-size: 13px; font-family: Verdana; float: left;">
        <div style="margin-bottom: 10px; margin-top: 10px; text-align: right;">
            <input id="refresh" type="button" value="Refresh" />
        </div>
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