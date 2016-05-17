angular.module('chatApp').service('CallbackUtils',  function(){

	var caminhoPadraoParaMensagem = 'data.message';

	var mensagemGenerica = 'Ocorreu um erro!';

	var obterConteudo = function(promise, caminhoParaMensagem){
		if(!caminhoParaMensagem){
			caminhoParaMensagem = caminhoPadraoParaMensagem;
		}
		var split = caminhoParaMensagem.split('.');
		for(var j = 0; j < split.length; j++){
			promise = promise[split[j]];
		}
		return promise;
	};

	var exibirMensagemGenerica = function(){
		alertify.error(mensagemGenerica);
	};

	var exibirMultiplasMensagens = function(mensagens){
		for(var i = 0; i < mensagens.length; i++) {
			alertify.error(mensagens[i]);
		}
	};

	var exibirMensagemUnica = function(mensagem){
		alertify.error(mensagem);
	};

	this.setMensagemGenerica = function(mensagem){
		mensagemGenerica = mensagem;
	};

	this.setCaminhoPadraoParaMensagem = function(caminhoPadrao){
		caminhoPadraoParaMensagem = caminhoPadrao;
	};

	this.mostrarErros = function(promise, caminhoParaMensagem){
		var conteudo = obterConteudo(promise, caminhoParaMensagem);
		
		if(typeof conteudo === 'string'){
			exibirMensagemUnica(conteudo);
		}else if(Array.isArray(conteudo)){
			exibirMultiplasMensagens(conteudo);
		}else{
			exibirMensagemGenerica();
		}
	}

});