from pyrfc import Connection, ABAPApplicationError, ABAPRuntimeError

class SAPConnector:
    def __init__(self, args):
        self.params = {
            'ashost': args.ashost,
            'sysnr': args.sysnr,
            'client': args.client,
            'user': args.user,
            'passwd': args.passwd,
        }

    def connect(self):
        try:
            connection = Connection(**self.params)
            return connection
        except (ABAPApplicationError, ABAPRuntimeError) as e:
            raise ConnectionError(f"SAP connection failed: {e}")
