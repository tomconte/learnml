''' Prepare the data.'''

import argparse
import logging
import os
import subprocess

import pandas as pd


def main():
    '''Main function.'''

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    print('# preparing', args.input, '->', args.output)

    # Unzip archive in source directory

    os.chdir(os.path.dirname(args.input))

    print('# extracting files...')

    subprocess.run(['tar', 'xzf', args.input], check=True)

    print('# extraction done')
    subprocess.run(['ls', '-la'], check=True)

    # Collect all files into one array

    all_posts = []

    for root, _, files in os.walk("20news-bydate-train"):
        if not files:
            continue
        group_name = root.split('/')[-1]
        print(group_name)
        for f in files:
            with open(os.path.join(root, f), 'r', errors='ignore') as fd:
                text = fd.read()

            # Skip all headers
            split_text = text.splitlines()
            for i in range(len(split_text)):
                if split_text[0] == "":
                    break
                del split_text[0]
            text = ' '.join(split_text)

            all_posts.append({
                'group': group_name,
                'text': text
            })

    df = pd.DataFrame(all_posts)

    dest_file = os.path.join(args.output, '20news-train.csv')
    print('# saving', dest_file)
    df.to_csv(dest_file, sep='\t')

    print('# output dir')
    subprocess.run(['ls', '-laR', args.output], check=True)

if __name__ == "__main__":
    main()
