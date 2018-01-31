# modify Cocos Copyright

## commit - log

  Commit: [script modify copyright, consider is cocos copyright or not](https://github.com/cocos2d/cocos2d-x/pull/18659/commits/aafd35f221a6c9b73b270ab502fe1a870d33770c)

  Log File: 20180129104517.log
  
## Install

```bash
pip install chardet
```

## Log Comments
1. __Done Before__
    
    found `Copyright (c) 2017-2018 Xiamen Yaji Software Co., Ltd.` in first comment block

1. __Modified OK__

    change 2017 to 2016, and add 2018 Yaji

```text
    Copyright (c) 2013-2017 Chukong Technologies Inc.
    ->
    Copyright (c) 2013-2016 Chukong Technologies Inc.
    Copyright (c) 2017-2018 Xiamen Yaji Software Co., Ltd.
```
2. __Template Add__
    
    No Copyright in file header, add [All Yaji Copyright](https://github.com/drelaptop/modifyCopyright/blob/master/cr_template.txt)

```text
    No Copyright
    ->
    add all Copyright content in Template File
```
3. __Single Add__

    add new line after cocos2d-x Copyright

```text
    Copyright (c) 2012 cocos2d-x.org
        
    ->
    Copyright (c) 2012 cocos2d-x.org
    Copyright (c) 2017-2018 Xiamen Yaji Software Co., Ltd.
```
4. __Add In Last__

    add new line and empty line before the main content of Detail Copyright

```text
    * Copyright (c) 2012 cocos2d-x.org
    * http://www.cocos2d-x.org
    *
    * Copyright 2012 Yannick Loriot. All rights reserved.
    * http://yannickloriot.com
    * 
    * Permission is hereby granted, ...
    ->
    * Copyright (c) 2012 cocos2d-x.org
    * http://www.cocos2d-x.org
    *
    * Copyright 2012 Yannick Loriot. All rights reserved.
    * http://yannickloriot.com
    * 
    * Copyright (c) 2017-2018 Xiamen Yaji Software Co., Ltd.
    * 
    * Permission is hereby granted,...
```

1. __Need Review__

    not any one of above items, mark this
