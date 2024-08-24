from collections import defaultdict
import re

# Utiliser un set pour les listes où l'ordre n'est pas important et où on doit vérifier les inclusions rapidement
checkedHosts = set()
exploits = set()
urls = set()
parsedUrls = set()

# Utiliser defaultdict pour des collections où des valeurs par défaut sont nécessaires
proxies = defaultdict(dict)

# Constantes
rfi_test_port = 8000
tOut = None
initialReqTime = 0
scriptName = ""
tempArg = ""
webDir = ""
skipsqli = False
previousPrint = ""
maxTimeout = None

# Les paramètres CSRF sont souvent vérifiés dans les formulaires, donc on les laisse en liste
csrf_params = [
    "csrf", "xsrf", "csrfmiddlewaretoken", "RequestVerificationToken",
    "_RequestVerificationToken", "antiForgeryToken", "authenticity_token",
    "csrf_token", "_csrf", "_xsrf", "_csrf_token", "_xsrf_token",
]

# Les chaînes de remplacement sont triées de la plus complexe à la moins complexe pour des remplacements efficaces
# Utilisation d'un tuple pour une immutabilité garantie
TO_REPLACE = (
    "Windows/System32/drivers/etc/hosts",
    "C%3A%5CWindows%5CSystem32%5Cdrivers%5Cetc%5Chosts",
    "file://C:\\Windows\\System32\\drivers\\etc\\hosts",
    "%5CWindows%5CSystem32%5Cdrivers%5Cetc%5Chosts",
    "C:\\Windows\\System32\\drivers\\etc\\hosts",
    "Windows\\System32\\drivers\\etc\\hosts",
    "%windir%\\System32\\drivers\\etc\\hosts",
    "file%3A%2F%2F%2Fetc%2Fpasswd%2500",
    "file%3A%2F%2F%2Fetc%2Fpasswd",
    "cat%24%7BIFS%7D%2Fetc%2Fpasswd",
    "cat%24IFS%2Fetc%2Fpasswd",
    "cat${IFS%??}/etc/passwd",
    "/sbin/cat%20/etc/passwd",
    "/sbin/cat /etc/passwd",
    "cat%20%2Fetc%2Fpasswd",
    "cat${IFS}/etc/passwd",
    "cat /etc/passwd",
    "%2Fetc%2Fpasswd",
    "/etc/passwd",
    "ysvznc",
    "ipconfig",
)

# Les mots-clés sont immuables, les listes sont donc transformées en tuples
KEY_WORDS = (
    "root:x:0:0", "<IMG sRC=X onerror=jaVaScRipT:alert`xss`>",
    "<img src=x onerror=javascript:alert`xss`>", "cm9vdDp4OjA",
    "Ond3dy1kYX", "ebbg:k:0:0", "d3d3LWRhdG", 'aahgpz"ptz>e<atzf',
    "jjj-qngn:k", "daemon:x:1:", "r o o t : x : 0 : 0", "ZGFlbW9uOng6",
    "; for 16-bit app support", "sample HOSTS file used by Microsoft",
    "iBvIG8gdCA6IHggOiA", "OyBmb3IgMTYtYml0IGFwcCBzdXBw",
    "c2FtcGxlIEhPU1RTIGZpbGUgIHVzZWQgYnkgTWljcm9zb2",
    "Windows IP Configuration", "OyBmb3IgMT", "; sbe 16-ovg ncc fhccbeg",
    "; sbe 16-ovg ncc fhccbeg", "fnzcyr UBFGF svyr hfrq ol Zvpebfbsg",
    ";  f o r  1 6 - b i t  a p p", "fnzcyr UBFGF svyr hfrq ol Zvpebfbsg",
    "c2FtcGxlIEhPU1RT", "=1943785348b45", "www-data:x", "PD9w",
    "961bb08a95dbc34397248d92352da799", "PCFET0NUWVBFIGh0b", "PCFET0N",
    "PGh0b",
)

# Fonction d'utilité pour la recherche de mots-clés dans un texte
def contains_keywords(text):
    """Retourne True si le texte contient l'un des mots-clés définis."""
    for keyword in KEY_WORDS:
        if keyword in text:
            return True
    return False

# Recherche de mots-clés avec expressions régulières (plus efficace pour certains patterns complexes)
compiled_keywords = re.compile('|'.join(map(re.escape, KEY_WORDS)))

def search_keywords(text):
    """Retourne les mots-clés trouvés dans le texte."""
    return compiled_keywords.findall(text)
