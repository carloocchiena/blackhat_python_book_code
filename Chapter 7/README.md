### Notes for the readers

This chapter is about a trojan interacting with our Github repo for updates.<br>

Since this book is about pentesting and security, I would be sure your GitHub account should have a 2FA. In that case you need to create a personal access token. It's not hard and you could follow along the instructions from GitHub itself https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token. 

The book suggest to create a folder structure within a test repository. I created this as well in this section, following along book instructions.<br>
Usual amount of optimization and cleaning was needed. The author seems to rush along every chapter leaving a lot of gaps here and there.<br>

For this chapter in particular I had a confrontation with EON Raider repository (https://github.com/EONRaider/blackhat-python3) to double check I got to a reasonable\correct routine.<br>

This chapter is also dedicated to show some git commands run from shell; this part has not been reproduced (obviously) here. <br>

The `imp` library the author is using is officially deprecated. You can go with `importlib` or even `types`.<br>
Check `imp` docs here https://docs.python.org/3/library/importlib.html#importlib.util.module_from_spec.<br>
Also: https://docs.python.org/3/library/imp.html

The Github wrapper could be found here https://github.com/copitux/python-github3
