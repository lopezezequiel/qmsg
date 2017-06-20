(function(root){

	var toQueryParams = function(data) {
		var params = [];
		for(var key in data) {
			params.push(encodeURIComponent(key) + "=" + 
				encodeURIComponent(data[key]));
		}
		return params.join("&");
	}


	var prepare = function(config) {
		
		var $config = {
			url: config.url,
			method: config.method || 'GET',
			data: config.data || {},
			timeout: config.timeout || 0,
			headers: {
				'CONTENT-TYPE': 'application/x-www-form-urlencoded;charset=UTF-8',
				'X-REQUESTED-WITH': 'XMLHttpRequest'
			},
			onerror: config.onerror,
			response: undefined,
			handlers: [],
			xhr: new XMLHttpRequest()
		}

		if($config.method === 'GET') {
			if($config.data) {
				$config.url += '?' + toQueryParams($config.data);
			}

			$config.data = null;
		}

		for(key in config.headers) {
			$config.headers[key.toUpperCase()] = config.headers[key];
		}

		if($config.headers['CONTENT-TYPE'].toLowerCase() === 
			'application/json') {
				$config.data = JSON.stringify($config.data);	
		}

		return $config;
	}


	var getResponse = function(xhr) {
		if(xhr.responseXML) {
			return xhr.responseXML;
		}
		try {
			return  JSON.parse(xhr.responseText);
		} catch(e) {
			return xhr.responseText;
		}
	}


	var sendRequest = function(config) {

		config.xhr.open(config.method, config.url, true);

		config.xhr.timeout = config.timeout;
		config.xhr.onerror = config.onerror;

		for(key in config.headers) {
			config.xhr.setRequestHeader(key, config.headers[key]);	
		}

		config.xhr.onreadystatechange = function () {
			if (config.xhr.readyState !== 4) return;

			config.response = getResponse(config.xhr);

			for(var i=0; i<config.handlers.length; i++) {
				executeHandler(config.handlers[i], config);
			}
		}
		
		config.xhr.send(config.data);
	}


	var isArray = function(object) {
		return Object.prototype.toString.call(object) === 
			'[object Array]';
	}


	var executeHandler = function(handler, config) {
		var codes = isArray(handler.codes) ? handler.codes : 
			[handler.codes];

		var negatives = [];
		var positives = [];

		for(var i=0; i<codes.length; i++) {
			if(codes[i] < 0) {
				negatives.push(-codes[i]);
			} else {
				positives.push(codes[i]);
			}
		}

		var status = config.xhr.status;

		if(negatives.length > 0 && negatives.indexOf(status) === -1) {
			handler.callback(config.response, config.xhr);
		} else if(positives.indexOf(status) !== -1) {
			handler.callback(config.response, config.xhr);
		}
	}


	root.ajax = function(config) {
		
		config = prepare(config);
		sendRequest(config);

		var ajax = {};

		ajax.handler = function(codes, callback) {
			
			var handler = {
				codes: codes, 
				callback: callback
			}

			if(typeof config.response === 'undefined') {
				config.handlers.push(handler);
			} else {
				executeHandler(handler, config);
			}
			
			return ajax;
		}
		
		return ajax;
	}
})(window);
