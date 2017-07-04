$("#search").click(function(){
	var text = $("#target").val();
	if(text == null || text==""||text==undefined||text=={}){
		alert('请输入检测文本');
		return false;
	} 
	$.ajax({
		   type:'post',
		   url: 'checkword.php',
		   data: {'text':text},
		   dataType:'json',
		   success: function(msg){	
			    if(msg == null || msg==""||msg==undefined||msg=={}){
			    	$("#result").html(text); 
				}else{
					var result = text;
					var keywords = '';
					var max=msg.length;
					for(var i=0;i<max;i++)
					{
						var replaceStr = msg[i];
						result = result.replace(new RegExp(replaceStr,'gm'),"<font style='color:red'>"+msg[i]+"</font>");
						keywords += '<input type="text" value="'+msg[i]+'" class="am-round keyword"/>'
					}
					$("#result").html(result);
					$("#keywordlist").html(keywords);
				}
		   },
		   error:function(textStatus){
			  alert("网络延迟，请刷新后重试！");
		   }
	});
})