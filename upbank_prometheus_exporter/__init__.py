import exporter, os
import up.api

if __name__ == '__main__':
	api = up.api.UP_API(os.getenv("TOKEN"))
	exp = exporter.Exporter(api)

	exp.run()	
