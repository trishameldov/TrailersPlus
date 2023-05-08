import { initFleetCF } from './fleet';
import { initCustomTrailerCF } from './custom-trailer';
import { initFoundLowerCF } from './found-lower';
import { initScheduleCF } from './schedule';
import { initWarrantyCF } from './warranty';

export function initForms() {
	initFleetCF();
	initCustomTrailerCF();
	initFoundLowerCF();
	initScheduleCF();
	initWarrantyCF();
}
