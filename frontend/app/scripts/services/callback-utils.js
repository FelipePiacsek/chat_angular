'use strict';
angular.module('chatApp').service('CallbackUtils',  function(){

	var caminhoPadraoParaMensagem = 'data.message';

	var mensagemGenerica = 'Ocorreu um erro!';

	var obterConteudo = function(promise, caminhoParaMensagem){
		if(!caminhoParaMensagem){
			caminhoParaMensagem = caminhoPadraoParaMensagem;
		}
		if(promise.status === -1){
			return null;
		}
		var split = caminhoParaMensagem.split('.');
		for(var j = 0; j < split.length; j++){
			promise = promise[split[j]];
		}
		return promise;
	};

	var mostrarMensagem = function(mensagem){
		//alertify.error(mensagem);
		alert(mensagem);
	};

	var exibirMensagemGenerica = function(){
		mostrarMensagem(mensagemGenerica);
	};

	var exibirMultiplasMensagens = function(mensagens){
		for(var i = 0; i < mensagens.length; i++) {
			mostrarMensagem(mensagens[i]);
		}
	};

	var exibirMensagemUnica = function(mensagem){
		mostrarMensagem(mensagem);
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