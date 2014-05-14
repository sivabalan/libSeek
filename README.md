libSeek
=======

Find software libraries in vogue

1. Run fetchProjects.py -> Creates projects_meta_data.json
2. Run FileFetcher.py -> Fetches all repositories (to repoData) in above json file in following format.
   Folder name : owner-repo
   Files within:    - metadata.json
                    - description.txt
                    - allPythonContent.py
3. Run generateDescriptionPfq.py -> Generates wordFrequencies.pfq for each repo.
4. Run IndexBuilder.py -> Creates alphabetical index json dumps to indexData from the pfq files