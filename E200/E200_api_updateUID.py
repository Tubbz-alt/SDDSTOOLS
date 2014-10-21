import numpy as _np
import h5py as _h5
import uuid as _uuid
import warnings
from mytools import Indent

def E200_api_updateUID(group,UID,value,verbose=False):
	indent = Indent.Indent()

	if _np.size(UID)>1:
		# ======================================
		# Run through list of UID's, processing
		# individually
		# ======================================
		Indent.vprint(indent,'Multiple UIDs entered, updating recursively')
		indent.level += 1

		# ======================================
		# Check for duplicate UIDs and sort
		# ======================================
		UID_sorted,inds = _np.unique(UID,return_index=True)
		value_sorted    = value[inds]
		if _np.size(UID_sorted) != _np.size(UID):
			raise ValueError('UIDs aren''t unique: {}'.format(UID))

		for i,uid in enumerate(UID_sorted):
			E200_api_updateUID(group,value=value_sorted[i],UID=uid,verbose=verbose)

	else:
	
		ref_dtype = _h5.special_dtype(ref=_h5.Reference)
	
		# ======================================
		# Get basic dsets
		# ======================================
		uid_dset  = group['UID']
		dat_dset  = group['dat']
		refs_dset = group['refs']
	
		uids      = uid_dset.value
		dat_refs  = dat_dset.value
	
		Indent.vprint(indent,'Adding UID: {}, value: {}'.format(UID,value))
		Indent.vprint(indent,'UID type is: {}'.format(type(UID)))
	
		# ======================================
		# Validate it's a numpy array
		# ======================================
		value = _np.array(value)
		
		# Verify vector
		# ndim = _np.ndim(value)
		# if ndim != 2:
		#         raise ValueError('Wrong dimensions for an array: {} dimensions'.format(ndim))
	
		# ======================================
		# Find matches
		# ======================================
		uid_match = _np.in1d(uids,UID)
		uid_match_total = _np.sum(uid_match)
		uid_match_inds = _np.where(uid_match)[0]
	
		if uid_match_total == 0:
			# ======================================
			# Add new UID and value
			# ======================================
			uuid_val = str(_uuid.uuid1())
			uuid_ref = refs_dset.create_dataset(name=uuid_val,data=value)
	
			uids_shape = uid_dset.shape
			
			uid_dset.resize((uids_shape[0]+1,))
			dat_dset.resize((uids_shape[0]+1,))
	
			uid_dset[-1] = UID
			dat_dset[-1] = uuid_ref.ref
	
		elif uid_match_total == 1:
			# ======================================
			# Delete old UID dataset
			# ======================================
			ind = uid_match_inds[0]
			ref = dat_dset.value[ind]
			ref_name = group.file[ref].name
			split = ref_name.split('/')
			ref_uuid = split[-1]
			del refs_dset[ref_uuid]
	
			# ======================================
			# Create new UUID dataset
			# ======================================
			uuid_val = str(_uuid.uuid1())
			uuid_ref = refs_dset.create_dataset(name=uuid_val,data=value)
	
			# ======================================
			# Replace reference
			# ======================================
			dat_dset[ind] = uuid_ref.ref
		elif uid_match_total > 1:
				# ======================================
				# Too many matches, corruption?
				# ======================================
				raise LookupError('Multiple unique IDs exist. ({} uids with values: {})'.format(uid_match_total,uids[uid_match]))
	
			# ======================================
			# Write changes to file
			# ======================================
		group.file.flush()
