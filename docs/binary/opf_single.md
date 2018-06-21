#### opf_single

+ **--use**  =>  use specific module.

exemple:

```
% sudo ./bin/opf_single.py --use software/search_sploit

help : print this bullet
run :    run argument
export : view exported result
argv :   view module arguments
set argument=value :  set argument from module
```

+ **--list** => listing of module name.

exemple:
```
- enterprise/viadeo_search :   Search possible employees list on Viadeo.com
- website/tools_suggester :   Find possible tools for exploitation of target.
- software/search_sploit :   Search exploit from selected software
- ip_address/vhost_IPchecker :   Find possible virtual host on selected ip address.
- ip_address/scan_nmap :   Scan open port from target ip address
- link/metatag_look :   Retrieve metatag from selected url
- website/cms_gathering :   Check if cms as used from selected website.
- website/file_common :   Read/Search common file on selected website.
- website/get_metadata_website :   Retrieve metatag from selected website
- person/get_enterprise_person :   Search possible enterprise for selected person
- link/get_email_link :   Search possible email address on selected page
- website/https_gathering :   Retrieve TLS/SSL information from selected website with SSLyze
- ip_address/get_opened_service :   Scan open service from target ip address
.......
```

