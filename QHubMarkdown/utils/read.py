from qtpy.QtCore import QFile, QIODevice

def readFileContent(filePath: str) -> str:
    file = QFile(filePath)
    
    if file.open(QIODevice.ReadOnly | QIODevice.Text):
        content = file.readAll().data().decode('utf-8')
        file.close()
        return content
    
    return ''