function[] = run_clustering(clus_name, input_file)

warning('off', 'all');

output_folder = '../Data/';

orig = spconvert(load(input_file));
orig(max(size(orig)),max(size(orig))) = 0;
orig_sym = orig + orig';
[i,j,k] = find(orig_sym);
orig_sym(i(find(k==2)),j(find(k==2))) = 1;
orig_sym_nodiag = orig_sym - diag(diag(orig_sym));

disp('==== Running clustering ====')
global model;
model = struct('code', {}, 'edges', {}, 'nodes1', {}, 'nodes2', {}, 'benefit', {}, 'benefit_notEnc', {}, 'quality', {}, 'alpha', {});
global model_idx;
model_idx = 0;

switch clus_name
    case 'slashburn'
         addpath('slashburn/');
         %output_slashburn = [input_file, '_slashburn.out']
         slashburn(orig_sym_nodiag, 2, output_folder, false, false, 3, input_file);
     case 'kcores'
         addpath('kcore/');
         addpath('kcore/gaimc/');
         output_kcores = [input_file, '_kcores.out'];
         diary(output_kcores);
         kcore(orig_sym_nodiag, output_folder, input_file);
         diary off;
     case 'louvain'
         [path, name, ext] = fileparts(input_file);
         tic
         system(['bash louvain/louvain.sh ', name, ext]);
         %LouvainEncode( orig_sym_nodiag, 2, output_model_greedy, false, false, 3, unweighted_graph);
         runtime = toc
     case 'Metis'
	     cd STRUCTURE_DISCOVERY_noNearStructs/Metis;
         tic
	     metis(['../../DATA/',dataname,'.',filetype],'../VariablePrecisionIntegers/VariablePrecisionIntegers/');
         MetisEncode( orig_sym_nodiag, 2, output_model_greedy, false, false, 3, unweighted_graph);
         runtime = toc
	     cd ..;
     case 'Spectral'
         cd STRUCTURE_DISCOVERY_noNearStructs/Spectral;
         %display(['../../DATA/',dataname,'.',filetype]);
         tic
         spectral_fact(['../../DATA/',dataname,'.',filetype]);
         SpectralEncode( orig_sym_nodiag, 2, output_model_greedy, false, false, 3, unweighted_graph);
         runtime = toc
         cd ..;
     case 'Hyperbolic'
         cd STRUCTURE_DISCOVERY_noNearStructs/Hyperbolic;
         tic
  	     system(['bash ./hyperbolic.sh ', dataname,'.',filetype, ' -> outputs in ../../VariablePrecisionIntegers/VariablePrecisionIntegers/']);
	     HyperbolicEncode( orig_sym_nodiag, 2, output_model_greedy, false, false, 3, unweighted_graph);
         runtime = toc
	     cd ..;
     case 'BlockModel'
         cd STRUCTURE_DISCOVERY_noNearStructs/BlockModel;
         tic
         blockmodel(['../../DATA/',dataname,'.',filetype]);
         BlockModelEncode( orig_sym_nodiag, 2, output_model_greedy, false, false, 3, unweighted_graph);
         runtime = toc
         cd ..;
     case 'BigClam'
         cd STRUCTURE_DISCOVERY_noNearStructs/BigClam;
         tic
         system(['bash ./bigclam.sh ', dataname,'.',filetype]);
         BigClamEncode( orig_sym_nodiag, 2, output_model_greedy, false, false, 3, unweighted_graph);
         runtime = toc
     otherwise
         warning('Wrong input, VoG_Reduced did not run.');
 end

 
% SlashBurnEncode( orig_sym_nodiag, 2, output_model_greedy, false, false, 3, unweighted_graph);
%delete(gcp);

%profile off;
%profsave(profile('info'),'vogprofile_results_memory_SL');

 quit
