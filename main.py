from utils import prepare_dataframe_xtandem, calc_PEP, get_output_basename, get_output_folder
from utils_figures import plot_outfigures
from pyteomics import auxiliary as aux
from os import path

def process_file(args):
    fname = args['file']
    outfolder = get_output_folder(args['o'], fname)
    outbasename = get_output_basename(fname)
    outfdr = args['fdr'] / 100
    print('Loading file %s...' % (path.basename(fname), ))
    df1 = prepare_dataframe_xtandem(fname, decoy_prefix=args['prefix'])
    df1 = calc_PEP(df1)
    df1 = df1[~df1['decoy1']]
    df1_f2 = aux.filter(df1, fdr=outfdr, key='PEP', is_decoy='decoy2', reverse=False, remove_decoy=True, ratio=0.5, correction=1)

    output_path_psms_full = path.join(outfolder, outbasename + '_PSMs_full.tsv')
    df1.to_csv(output_path_psms_full, sep='\t', index=False)

    output_path_psms = path.join(outfolder, outbasename + '_PSMs.tsv')
    df1_f2.to_csv(output_path_psms, sep='\t', index=False)

    df1_peptides = df1.sort_values('PEP', ascending=True).drop_duplicates(['peptide'])
    df1_peptides_f = aux.filter(df1_peptides, fdr=outfdr, key='PEP', is_decoy='decoy2', reverse=False, remove_decoy=True, ratio=0.5, correction=1)
    output_path_peptides = path.join(outfolder, outbasename + '_peptides.tsv')
    df1_peptides_f.to_csv(output_path_peptides, sep='\t', index=False)

    plot_outfigures(df1, df1_f2, df1_peptides, df1_peptides_f, outfolder, outbasename)